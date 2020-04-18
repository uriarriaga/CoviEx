import flask, requests, json, funciones
from flask import request

def sendWebexMsg(texto):
    url = "https://api.ciscospark.com/v1/messages"
    idRoomTodos = "Y2lzY29zcGFyazovL3VzL1JPT00vNjFiYTM4ZDAtNzQzZS0xMWVhLTg1YzMtODM5MjNiY2UxMjFm"
    idRoomYo = "Y2lzY29zcGFyazovL3VzL1JPT00vMTRkMzU4OGQtNzBkNi0zZDRkLWFkMDMtNmEzZGE2NjNjMjUw"
    payload = {"text": texto,"roomId": idRoomYo}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ZTNjZjBiZTMtNjhmOC00ODJkLTg3MzAtMjg0MTAxNDBlNWY4MDljYTkwMmQtNGY0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
    }
    requests.post( url, headers=headers, json = payload)


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/login')
def buttonPressFront():
    sendWebexMsg("login")
    with open("templates/respuestaWebexTeams.html") as file: 
        data = file.read()
    return data

@app.route('/widget')
def Widget():
    #sendWebexMsg("widget")
    with open("templates/widget.html") as file: 
        data = file.read()
    return data

@app.route('/demo')
def demo():
    #sendWebexMsg("widget")
    with open("templates/widget.html") as file: 
        data = file.read()
    return data

@app.route('/respuestateleconsulta')
def respuestateleconsulta():
    #sendWebexMsg("widget")
    with open("templates/widget.html") as file: 
        data = file.read()
    return data

@app.route('/respuestatelevisita')
def respuestatelevisita():
    #sendWebexMsg("widget")
    with open("templates/widget.html") as file: 
        data = file.read()
    return data

@app.route('/', methods=['GET'])
def home():
    with open("templates/Frontend.html") as file: 
        data = file.read()
    return data


app.run(host="0.0.0.0")   