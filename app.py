import flask, requests, json
from flask import request, redirect, url_for
from funciones import sendWebexMsg, sendSMS



app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/login')
def login():
    with open("templates/login.html") as file: 
        data = file.read()
    return data

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

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")   