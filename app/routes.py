from flask import request, redirect, url_for, render_template, flash, session ,  jsonify
from app import app, db, Base, Familiar, GuestUser, Paciente, Agenda
from app.funciones import sendWebexMsg, sendSMS, createJWT, generarWebex
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

                return redirect(url_for('demo'))

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
    print(invitado.username,invitado.expirationTime)
    if invitado.expirationTime <= datetime.utcnow().timestamp():
        return render_template('widgetexpired.html', title='widget')
    JWToken = createJWT(invitado.user_id,invitado.expirationTime,invitado.secret)
    return render_template('widget.html', title='widget', token=JWToken, SIP=invitado.correo)



#///////// ////// ADMIN ////// ////// //////   




@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.admin:
        return redirect(url_for('demo'))


        
    formusr = userForm()
    print(formusr.username.data)
  
    if formusr.validate_on_submit():
       
        print(formusr.username.data)
        usr = User(username = formusr.username.data,email = formusr.email.data,password = formusr.password.data,
                    admin = formusr.admin.data,    atencionDomiciliaria = formusr.ad.data,
                    informeMedico = formusr.im.data, teleVisita = formusr.tv.data,  capturista= formusr.cp.data)
        db.session.add(usr)
        db.session.commit() 
    return render_template('admin.html', form = formusr)

@app.route('/insertdata', methods=['GET', 'POST'])
#@login_required
def insertdata():

    json_data = request.get_data()
    print(json_data)
    
  #  paciente = Paciente()
  #  paciente.nombre = str(json_data["nombre_paciente"])
  #  paciente.celular = str(json_data["celular_paciente"])
  #  paciente.email = str(json_data["email_paciente"])

   # db.session.add(paciente)
   # db.session.commit()

   # paciente_db = db.session.query(Paciente).filter_by(email=paciente.email).first()
   # paciente_id_db = str(paciente_db.id)


#    familiares_paciente = json_data["familiares"]

#    for item in familiares_paciente:
#        familiar = Familiar()
#
#        familiar.nombre = str(item["nombre_familiar"])
#        familiar.celular = str(item["celular_familiar"])
#        familiar.email = str(item["email_familiar"])
#        familiar.id_paciente = paciente_id_db

 #       db.session.add(familiar)

 #   db.session.commit()
        
    return str(json_data)

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



# ////////////////////  Demos ///////////////

@app.route('/demo')
@login_required
def demo():
    if current_user.admin:
        return redirect(url_for('admin'))
    return render_template('demo.html')


@app.route('/democonstula', methods=['GET', 'POST'])
@login_required
def teleconsulta():
    if current_user.admin:
        return redirect(url_for('admin'))


    return render_template('democonstula.html')


@app.route('/demovisita', methods=['GET', 'POST'])
@login_required
def demovisita():
    if current_user.admin:
        return redirect(url_for('admin'))
   

    #if current_user.username != "debug":
        #sendSMS(numero)
        #return redirect(url_for('respuestatelevisita'))

    return render_template('demovisita.html')



@app.route('/demoinformemedico', methods=['GET', 'POST'])
@login_required
def demoinformemedico():
    if current_user.admin:
        return redirect(url_for('admin'))
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        if current_user.username != "debug":
            sendSMS(numero)
        return redirect(url_for('respuestainforme'))
    return render_template('demoinformemedico.html', form = formv)



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
    return redirect(url_for("demo"))

# //////////////////// LLAMADAS APIs ///////////// /////// /////// /////// /////// 


@app.route('/getpacientes', methods=['GET', 'POST'])
@login_required
def getpacientes():
    pacients =  db.session.query(Paciente).all()

    list =  "{"  +  '"' + 'pacientes' + '"' + ":" + "["
    for patient in pacients:
        print(str(patient.nombre))
        list +="{"+ '"' + "nombre" + '"'+":"+ '"'+ patient.nombre + '"'+ "," + '"' + "celular" + '"'+":"+ '"'+ patient.celular + '"'+ "," + '"' +"email" + '"'+":"+ '"' + patient.email + '"'+ "," + '"' +"id" + '"'+":"+ '"' + str(patient.id) + '"'+ "},"
    list = list[:-1]  
    list += "]}"  

    listx = list.strip()

    y = json.loads(list)

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


    generarWebex(celulares,email)

    #llamar funcoin envio de sms de uri todo en epoc
    # datetime
    #generarWebex(["listaNumeros"],"correo")
    return data


@app.route('/agendarllamada', methods=['GET', 'POST'])
@login_required
def agendarllamada():

    data = request.get_data()

    call = json.loads(data)




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

    d = datetime.strptime(inDate, "%d/%m/%Y  %H:%M") 
    #dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    #01/05/2020 9:44
    
    print('------------------------------------------------------------------')
    print(d)
  
    print(d.timestamp())
    print(str(celulares))
    print('------------------------------------------------------------------')

    if tipo == "1":

        #insertas el id del paciente en la tabla
        print("tipo de meeting 1:1")
        meeting = Agenda(fecha_hora = d.timestamp(), email = current_user.email, id_user = current_user.id,
                    id_paciente = ids_[0],    id_servicio = tipo,
                    celulares =  str(celulares) )
        db.session.add(meeting)
        db.session.commit() 


    else:
        
        print("tipo de meeting 1:X")
        # Insertas la cita y despues insertas el id de los pacientes con las citas
        meeting = Agenda(fecha_hora = d.timestamp(), email = current_user.email,
        id_user = current_user.id,id_servicio = tipo, celulares = str(celulares),id_paciente = "" )
        db.session.add(meeting)
        db.session.commit() 

    #insertar los datos de la video llamada
    return data

