import flask, requests, json
from flask import request, redirect, url_for, render_template, flash
from funciones import sendWebexMsg, sendSMS
from forms import LoginForm



app = flask.Flask(__name__)
app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["DEBUG"] = True

jwtPayload = {
  "sub": "TestTeleconsulta",
  "name": "TestTeleconsulta",
  "iss": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9kYjJjZmI0Ny02MDJiLTRmNGEtODNhMS04MDExZDM4MjdjMzM",
  "exp": "1587366980"
}
jwtSecret = "jyxr2LIZwke2X3IQA9Ui+oqDrG6Fwy7pbAe92DJf51Q="

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "joarriag"  and form.password.data == "cisco123":
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('index'))
        else:
            flash('Login requested for user login Unsuccesful. Plese check username and password')
    return render_template('loginTut.html', title='Sign In', form=form)


@app.route('/widget')
def Widget():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0VGVsZWNvbnN1bHRhIiwibmFtZSI6IlRlc3RUZWxlY29uc3VsdGEiLCJpc3MiOiJZMmx6WTI5emNHRnlhem92TDNWekwwOVNSMEZPU1ZwQlZFbFBUaTlrWWpKalptSTBOeTAyTURKaUxUUm1OR0V0T0ROaE1TMDRNREV4WkRNNE1qZGpNek0iLCJleHAiOiIxNTkyNjM3MDgwIn0.bbcFiX7bywA8ExWmuSHIys36TDVzlIOswE3llnPtqYM"
    return render_template('widget.html', title='Widget', token=token)

@app.route('/democonstula')
def democonstula():
    return render_template('democonstula.html', title='democonstula')

@app.route('/demovisita')
def demovisita():
    return render_template('demovisita.html', title='democonstula')

@app.route('/repuestateleconsulta')
def respuestateleconsulta():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('repuestateleconsulta.html', title='repuestateleconsulta')

@app.route('/respuestatelevisita')
def respuestatelevisita():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('repuestatelevisita.html', title='respuestatelevisita')
     


@app.route('/')
@app.route('/demo')
def demo():
    user = {'username': 'Miguel'}
    return render_template('demo.html', title='Home', user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0")   