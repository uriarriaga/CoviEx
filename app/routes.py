from flask import request, redirect, url_for, render_template, flash, session 
from app import app
from app.funciones import sendWebexMsg, sendSMS
from app.forms import LoginForm, smsForm, userForm
from app.models import User, GuestUser
from flask_login import login_user, logout_user, login_required

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
    actualTimePlusHR = calendar.timegm(time.gmtime())+3600
    print(calendar.timegm(time.gmtime()),actualTimePlusHR)
    payload = {
    "sub": "TestTeleconsulta",
    "name": "TestTeleconsulta",
    "iss": invitado.user_id,
    "exp": str(calendar.timegm(time.gmtime())+3600)
    }
    headers= { 
    "alg": "HS256",
    "typ": "JWT" 
    }
    encoded = jwt.encode(payload, key64, algorithm ='HS256', headers=headers).decode("utf-8")
    print(str(encoded))
    decoded = jwt.decode(encoded, key64, algorithms ='HS256')
    print( decoded["exp"],calendar.timegm(time.gmtime()))
    if int(calendar.timegm(time.gmtime())) <= int(decoded["exp"]):
        return render_template('widgetexpired.html', title='widget')
    token = encoded
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0VGVsZWNvbnN1bHRhIiwibmFtZSI6IlRlc3RUZWxlY29uc3VsdGEiLCJpc3MiOiJZMmx6WTI5emNHRnlhem92TDNWekwwOVNSMEZPU1ZwQlZFbFBUaTlrWWpKalptSTBOeTAyTURKaUxUUm1OR0V0T0ROaE1TMDRNREV4WkRNNE1qZGpNek0iLCJleHAiOiIxNTkyNjM3MDgwIn0.bbcFiX7bywA8ExWmuSHIys36TDVzlIOswE3llnPtqYM"
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
        sendSMS(numero)
        return redirect(url_for('respuestateleconsulta'))
    return render_template('democonstula.html', form = form)

@app.route('/demovisita', methods=['GET', 'POST'])
@login_required
def demovisita():
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        sendSMS(numero)
        return redirect(url_for('respuestateleconsulta'))
    return render_template('demovisita.html', form = formv)



@app.route('/demoinformemedico', methods=['GET', 'POST'])
@login_required
def demoinformemedico():
    formv = smsForm()
    if formv.validate_on_submit():
        numero = "+521"+formv.sms.data
        sendSMS(numero)
        return redirect(url_for('respuestainforme'))
    return render_template('demoinformemedico.html', form = formv)



@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    formv = userForm()
    return render_template('admin.html', form = formv)



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
