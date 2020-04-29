from flask import request, redirect, url_for, render_template, flash, session 
from app import app, db
from app.funciones import sendWebexMsg, sendSMS
from app.forms import LoginForm, smsForm, userForm
from app.models import User, GuestUser
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user

import jwt 
import base64
import time,calendar


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('demo'))
        else:
            flash('Login requested for user login Unsuccesful. Plese check username and password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/widget')
def Widget():
    token = request.args.get('token')
    invitado = GuestUser.query.first()
    key64 = base64.b64decode(invitado.secret)
    try:
        decoded = jwt.decode(token, key64, algorithms ='HS256')
    except:
        return render_template('widgetexpired.html', title='widget')
    print( time.gmtime(int(decoded["exp"])))
    return render_template('widget.html', title='widget', token=token)

@app.route('/demo')
@login_required
def demo():
    return render_template('demo.html')

# ////////////////////  Demos ///////////////
@app.route('/democonstula', methods=['GET', 'POST'])
@login_required
def teleconsulta():
    form = smsForm()
    if form.validate_on_submit():
        numero = "+521"+form.sms.data
        if current_user.username != "debug":
            sendSMS(numero)
        return redirect(url_for('respuestateleconsulta'))
    return render_template('democonstula.html', form = form)

@app.route('/demovisita', methods=['GET', 'POST'])
@login_required
def demovisita():
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        if current_user.username != "debug":
            sendSMS(numero)
        return redirect(url_for('respuestatelevisita'))
    return render_template('demovisita.html', form = formv)



@app.route('/demoinformemedico', methods=['GET', 'POST'])
@login_required
def demoinformemedico():
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        if current_user.username != "debug":
            sendSMS(numero)
        return redirect(url_for('respuestainforme'))
    return render_template('demoinformemedico.html', form = formv)



@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    formusr = userForm()
    print(formusr.username.data)
    print("entro a adminx")
    if formusr.validate_on_submit():
        print("entro a submit")
        print(formusr.username.data)
        usr = User(username = formusr.username.data,email = formusr.email.data,password = formusr.password.data,
                    admin = formusr.admin.data,    atencionDomiciliaria = formusr.ad.data,
                    informeMedico = formusr.im.data, teleVisita = formusr.tv.data)
        db.session.add(usr)
        db.session.commit()
    return render_template('admin.html', form = formusr)

@app.route('/capture', methods=['GET', 'POST'])
@login_required
def capture():
    formv = userForm()
    return render_template('capture.html', form = formv)



# //////////////////// Respuestas ///////////// 
@app.route('/respuestateleconsulta')
@login_required
def respuestateleconsulta():
    return render_template('respuestateleconsulta.html')

@app.route('/respuestatelevisita')
@login_required
def respuestatelevisita():
    return render_template('respuestatelevisita.html', title='respuestatelevisita')

@app.route('/respuestainforme')
@login_required
def respuestainforme():
    return render_template('respuestainforme.html', title='respuestainforme')
     

@app.route('/')
def index():
    return redirect(url_for("demo"))
