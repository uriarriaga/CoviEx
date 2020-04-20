import flask, requests, json
from flask import request, redirect, url_for, render_template, flash
from funciones import sendWebexMsg, sendSMS
from forms import LoginForm



app = flask.Flask(__name__)
app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["DEBUG"] = True


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
    with open("templates/widget.html") as file: 
        data = file.read()
    return data

@app.route('/democonstula')
def demo():
    with open("templates/democonstula.html") as file: 
        data = file.read()
    return data

@app.route('/repuestateleconsulta')
def respuestateleconsulta():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    sendSMS(directorio)
    with open("templates/repuestateleconsulta.html") as file: 
        data = file.read()
    return data

@app.route('/respuestatelevisita')
def respuestatelevisita():
    with open("templates/widget.html") as file: 
        data = file.read()
    return data


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0")   