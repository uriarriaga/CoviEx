from flask import request, redirect, url_for, render_template, flash, session ,  jsonify
from app import app, db, Base, Familiar, GuestUser, Paciente, Agenda
from app.funciones import sendWebexMsg, sendSMS, createJWT, generarWebex, existeWebex,agendarWebex, hostJoined, cronSMS, sendAgendaSMS
from app.forms import LoginForm, smsForm, userForm,capturesForm, PacienteForm, PacientesForm
from app.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime



import jwt 
import base64
import time,calendar
import json
from json import JSONEncoder




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            if not current_user.admin:
               

                if current_user.capturista:
                    print(current_user.capturista)
                    print('entro a capturista')
                    return redirect(url_for('capture'))

                return redirect(url_for('appdoctor'))

            else:
                return redirect(url_for('admin'))

      
        else:
            flash('Login requested for user login Unsuccesful. Plese check username and password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/widget')
def widget():
    token = request.args.get('token')
    invitado = db.session.query(GuestUser).filter_by(indentficadorTemporal=token).first() 
    if invitado is None:
        return render_template('widgetexpired.html', title='widget')
    if invitado.expirationTime <= datetime.utcnow().timestamp():
        print(invitado.username,invitado.expirationTime)
        return render_template('widgetexpired.html', title='widget')
    if not hostJoined(invitado.correo.split("@")[0]):
        return render_template('widgetLobby.html', title='widget')
    JWToken = createJWT(invitado.user_id,invitado.expirationTime,invitado.secret)
    return render_template('llamadaSDK.html', title='widget', token=JWToken, SIP=invitado.correo)

@app.route('/cronisticamente')
def cron():
    return str(cronSMS())

#///////// ////// ADMIN ////// ////// //////   




@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():

    if not current_user.admin:
        return redirect(url_for('appdoctor'))

        
    formusr = userForm()
    print(formusr.username.data)

    if formusr.validate_on_submit():

        if  formusr.admin.data != 0 or formusr.ad.data != 0 or formusr.cp.data != 0  :

            if  existeWebex(formusr.email.data) or formusr.admin.data == 1 or formusr.cp.data ==1 :

                user_ = User.query.filter_by(username=formusr.username.data).first()


                try:
                    if user_.username == formusr.username.data:
                        flash('El nombre de usuario ya existe')

                except:
                

                    userx = User.query.filter_by(email=formusr.email.data).first()

                    try:

                        if userx.email == formusr.email.data:
                            flash('El email de usuario ya existe')

                    except:

                        print(formusr.username.data)
                        usr = User(username = formusr.username.data,email = formusr.email.data,password = formusr.password.data,
                                    admin = formusr.admin.data,    atenciondomiciliaria = formusr.ad.data,
                                    informeMedico = formusr.im.data, teleVisita = formusr.tv.data,  capturista= formusr.cp.data)
                        db.session.add(usr)
                        db.session.commit()
                        flash('Usuario insertado de forma correcta!')

            else:
                flash('Correo no valido o no regitrado en Webex')

        else:
            flash('Para poder insertar un usuario por favor seleccione el tipo de usuario en la sección de permisos')

    return render_template('admin.html', form = formusr)

@app.route('/insertdata', methods=['GET', 'POST'])
#@login_required
def insertdata():

    json_data = request.get_data()
    json_data = json.loads(json_data)

    action = str(json_data["action"])
    paciente_id = str(json_data["paciente_id"])

    print("-----------------------------------------------------------")
    print("Action : " + str(action))
    print("-----------------------------------------------------------")

    if action == "update":
        print("-----------------------------------------------------------")
        print("Entro a Update")
        print("-----------------------------------------------------------")


        #consulta el id en base al json (celular) 

        #paciente_id_db = db.session.query(Paciente).filter_by(celular=str(json_data["celular_paciente"])).first()
        #paciente_id = paciente_id_db.id


        print("Entro a Update Paciente")

        paciente_db = db.session.query(Paciente).filter_by(id=paciente_id).first()

        print(str(json_data["nombre_paciente"]))

        #paciente_db.id 
        paciente_db.nombre = str(json_data["nombre_paciente"])
        paciente_db.celular = str(json_data["celular_paciente"])
        paciente_db.email = str(json_data["email_paciente"])

        db.session.commit()

        #Eliminar usuarios de base de datos:

        familiares_db = db.session.query(Familiar).filter_by(id_paciente=paciente_id)

        for familiar in familiares_db:

            db.session.query(Familiar).filter(Familiar.id_paciente==paciente_id).delete()

        db.session.commit()

        familiares_paciente = json_data["familiares_paciente"]

        for item in familiares_paciente:

            familiar = Familiar()
            familiar.nombre = str(item["nombre_familiar"])
            familiar.celular = str(item["celular_familiar"])
            familiar.email = str(item["email_familiar"])
            familiar.id_paciente = paciente_db.id
            db.session.add(familiar)

        db.session.commit()

    else:

        print("-----------------------------------------------------------")
        print("Entro a Insert")
        print("-----------------------------------------------------------")

        paciente = Paciente()

        paciente.nombre = str(json_data["nombre_paciente"])
        paciente.celular = str(json_data["celular_paciente"])
        paciente.email = str(json_data["email_paciente"])

        db.session.add(paciente)
        db.session.commit()

        paciente_db = db.session.query(Paciente).filter_by(email=paciente.email).first()
        paciente_id_db = str(paciente_db.id)

        familiares_paciente = json_data["familiares_paciente"]

        for item in familiares_paciente:

            familiar = Familiar()
            familiar.nombre = str(item["nombre_familiar"])
            familiar.celular = str(item["celular_familiar"])
            familiar.email = str(item["email_familiar"])
            familiar.id_paciente = paciente_id_db
            db.session.add(familiar)


        db.session.commit()

    return "json_data OK"

@app.route('/capture', methods=['GET', 'POST'])
@login_required
def capture():
    if not current_user.capturista:
        return redirect(url_for('login'))
    formv = userForm()
    fam  = Familiar(nombre = "pruebamemo",celular="7222849367",email="mr.memo@gmail.com",id_paciente=1)
    pac = Paciente(nombre = "pruebamemo",celular="7222849367",email="mr.memo@gmail.com")
    #db.session.add(fam)
    #db.session.commit()
    #app.after_request(sql_debug)
    #return"<h2>Done!</h>"
    return render_template('capture.html')



# ////////////////////  appdoctors ///////////////

@app.route('/appdoctor')
@login_required
def appdoctor():
    if current_user.admin:
        return redirect(url_for('admin'))
    return render_template('appdoctor.html')


@app.route('/appdoctorconstula', methods=['GET', 'POST'])
@login_required
def teleconsulta():
    if current_user.admin:
        return redirect(url_for('admin'))


    return render_template('appdoctorconstula.html')


@app.route('/appdoctorvisita', methods=['GET', 'POST'])
@login_required
def appdoctorvisita():
    if current_user.admin:
        return redirect(url_for('admin'))
   

    #if current_user.username != "debug":
        #sendSMS(numero)
        #return redirect(url_for('respuestatelevisita'))

    return render_template('appdoctorvisita.html')



@app.route('/appdoctorinformemedico', methods=['GET', 'POST'])
@login_required
def appdoctorinformemedico():
    if current_user.admin:
        return redirect(url_for('admin'))
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        if current_user.username != "debug":
            sendSMS(numero)
        return redirect(url_for('respuestainforme'))
    return render_template('appdoctorinformemedico.html', form = formv)



# //////////////////// Respuestas ///////////// 
@app.route('/respuestateleconsulta')
@login_required
def respuestateleconsulta():
    if current_user.admin:
        return redirect(url_for('admin'))
    return render_template('respuestateleconsulta.html')

@app.route('/respuestatelevisita')
@login_required
def respuestatelevisita():
    if current_user.admin:
        return redirect(url_for('admin'))
    return render_template('respuestatelevisita.html', title='respuestatelevisita')

@app.route('/respuestainforme')
@login_required
def respuestainforme():
    if current_user.admin:
        return redirect(url_for('admin'))
    return render_template('respuestainforme.html', title='respuestainforme')
     

@app.route('/')
def index():
    return redirect(url_for('appdoctor'))

# //////////////////// LLAMADAS APIs ///////////// /////// /////// /////// /////// 


@app.route('/getpacientes', methods=['GET', 'POST'])
@login_required
def getpacientes():
    pacients =  db.session.query(Paciente).all()

    # // lineas para el tema de DB sin tados
    list = ""
    listx =""
    # if a pacients list is 0 ??? 
    if len(pacients) == 0:
        print("NUMERO DE PACIENTES: " +str(len(pacients)))
        return "bd_0"

    else:

        print("NUMERO DE PACIENTES: " +str(len(pacients)))

        list =  "{"  +  '"' + 'pacientes' + '"' + ":" + "["
        for patient in pacients:
            print(str(patient.nombre))
            list +="{"+ '"' + "nombre" + '"'+":"+ '"'+ patient.nombre + '"'+ "," + '"' + "celular" + '"'+":"+ '"'+ patient.celular + '"'+ "," + '"' +"email" + '"'+":"+ '"' + patient.email + '"'+ "," + '"' +"id" + '"'+":"+ '"' + str(patient.id) + '"'+ "},"
        list = list[:-1]  
        list += "]}"  

        listx = list.strip()

    #print("------------" + y["employees"][0]["nombre"])

        print(list)     
        return listx


@app.route('/getfamiliares', methods=['GET', 'POST'])
@login_required
def getfamiliares():
    familiares =  db.session.query(Familiar).all()

    list =  "{"  +  '"' + 'familiares' + '"' + ":" + "["
    for familiar in familiares:
        print(str(familiar.nombre))
        list +="{"+ '"' + "nombre" + '"'+":"+ '"'+ familiar.nombre + '"'+ "," + '"' + "celular" + '"'+":"+ '"'+ familiar.celular + '"'+ "," + '"' +"email" + '"'+":"+ '"' + familiar.email + '"'+ "," + '"' +"id" + '"'+":"+ '"' + str(familiar.id) + '"'+ "," + '"' +"id_paciente" + '"'+":"+ '"' + str(familiar.id_paciente) + '"'+ "},"
    list = list[:-1]  
    list += "]}"  

    listx = list.strip()

    y = json.loads(list)

    #print("------------" + y["employees"][0]["nombre"])

    print(list)     
    return listx


@app.route('/getusuarios', methods=['GET', 'POST'])
@login_required
def getusuarios():

    usuarios =  db.session.query(User).all()

    list =  "{"  +  '"' + 'usuarios' + '"' + ":" + "["
    for usuario in usuarios:
        #print(str(familiar.nombre))
        list +="{"+ '"' + "username" + '"'+":"+ '"'+ usuario.username + '"'+ "," + '"' + "email" + '"'+":"+ '"'+ usuario.email + '"'+ "," + '"' +"admin" + '"'+":"+ '"' + str(usuario.admin) + '"'+ "," + '"' +"id" + '"'+":"+ '"' + str(usuario.id) + '"'+ "," + '"' +"Medico" + '"'+":"+ '"' + str(usuario.atenciondomiciliaria) + '"'+  "," + '"' +"Capturista" + '"'+":"+ '"' + str(usuario.capturista) + '"'  "," + '"' + "password" + '"'+":"+ '"'+ usuario.password + '"'+"},"
    list = list[:-1]  
    list += "]}"  

    listx = list.strip()

    y = json.loads(list)

    #print("------------" + y["employees"][0]["nombre"])

    print(list)     
    return listx



@app.route('/delusuario', methods=['GET', 'POST'])
@login_required
def delusuarios():

    data = request.get_data()
    usuario = json.loads(data)
    usuario_id=usuario['id']
    print('XXXXXXXXXXXXXXXXXXXXXXX' + str(usuario_id))

    db.session.query(User).filter(User.id==usuario_id).delete() 
    db.session.commit()
  
    return data


@app.route('/llamada', methods=['GET', 'POST'])
@login_required
def llamada():
    
    data = request.get_data()

    call = json.loads(data)
    celulares = []

    lista = call["datos"]
    for elemento in lista:
        celulares.append(elemento["celular"])

    email = current_user.email

    nombre = call["name"]
    tipo = call["tipo"]
    print("EMAIL   -----  >" + email + "nombre   ------   >" + nombre + "celulares   - - - -   >"  + str(celulares))

    if tipo == "1":
        generarWebex(celulares,email, "Atencion domiciliaria " + nombre)
    if tipo == "2":
        generarWebex(celulares,email, "Informe Medico " + nombre)
    if tipo == "3":
        generarWebex(celulares,email, "TeleVisita " + nombre)

    #llamar funcoin envio de sms de uri todo en epoc
    # datetime
    #generarWebex(["listaNumeros"],"correo")
    return data


@app.route('/agendarllamada', methods=['GET', 'POST'])
@login_required
def agendarllamada():

    data = request.get_data()

    call = json.loads(data)

    SIP = ""

    email = current_user.email

    celulares = []

    ids_ = []

    lista = call["datos"]
    for elemento in lista:
        celulares.append(elemento["celular"]) 
        ids_.append((elemento["id"]))

    print('------------------------------------------------------------------')
    print ("correo:  " + current_user.email)
    print ("celulares:  " + str(celulares))

    inDate = call["Fecha"]
    tipo = call["tipo"]
    nombre = call["name"]
    


    d = datetime.strptime(inDate, "%d/%m/%Y %H:%M") 

    #dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    #01/05/2020 9:44
    
    print('------------------------------------------------------------------')
    print(d)
    utctime = int(d.timestamp())
    print("UTC timestamp :" +  str(utctime))
    print(str(celulares))
    print('------------------------------------------------------------------' + tipo)

    if tipo == "1":

        #insertas el id del paciente en la tabla
        print("tipo de meeting 1:1")



        SIP = agendarWebex(celulares,email, "Atencion domiciliaria " + nombre, utctime)

        if SIP != None :

            meeting = Agenda(fecha_hora = utctime, email = current_user.email, id_user = current_user.id,
            id_paciente = ids_[0],    id_servicio = tipo,
            celulares =  str(",".join(celulares)), SIP = SIP)
            db.session.add(meeting)
            db.session.commit()
            sendAgendaSMS(celulares,d,"Atencion domiciliaria ")

        else:

            return"error"


    else:
        
        id_paciete = call["id_paciente"]
        
        if tipo == "2":
            #llamar a la funcion de uriel con el tipo de servicio de informe medico
            print("Informe Medico")
            
            SIP = agendarWebex(celulares,email, "Informe Medico " + nombre, utctime)

            if SIP != None :

                meeting = Agenda(fecha_hora = utctime, email = current_user.email,
                id_user = current_user.id,id_servicio = tipo, celulares = str(",".join(celulares)),id_paciente = int(id_paciete), SIP = SIP )
                db.session.add(meeting)
                db.session.commit()
                sendAgendaSMS(celulares,d,"Informe Medico ")

            else:

                return"error"



        if tipo == "3":
            #llamar a la funcion de uriel con el tipo de servicio de Televistia
            print("TeleVistia")

            SIP = agendarWebex(celulares,email, "TeleVisita" + nombre, utctime)

            if SIP != None :

                meeting = Agenda(fecha_hora = utctime, email = current_user.email,
                id_user = current_user.id,id_servicio = tipo, celulares = str(",".join(celulares)),id_paciente = int(id_paciete), SIP = SIP )
                db.session.add(meeting)
                db.session.commit()
                sendAgendaSMS(celulares,d,"TeleVisita ")

            else:

                return"error"
        

        print("tipo de meeting 1:X")
        # Insertas la cita y despues insertas el id de los pacientes con las citas


    #insertar los datos de la video llamada



    return data

