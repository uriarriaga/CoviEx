import requests, os, jwt, xmltodict

from app.models import User
from app import GuestUser
from datetime import datetime
from app import db  
from secrets import token_urlsafe
import jwt 
import base64
import time,calendar

from dotenv import load_dotenv
load_dotenv()


def sendWebexMsg(texto,roomId=os.environ["idRoomYo"]):
    payload = {"text": texto,"roomId": roomId   }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ os.environ["botToken"]
    }
    requests.post( os.environ["urlWebextTeams"], headers=headers, json = payload )

def createWebexMeeting():
    import requests
    with open("app/createMeetings.xml") as file: 
        data = file.read()
    url = "https://api.webex.com/WBXService/XMLService"
    payload = data.format("prueba_Uriel")
    headers = {
    'Content-Type': 'text/plain'
    }
    response = requests.post( url, headers=headers, data = payload).text
    #print(str(response["serv:message"]["serv:header"]["serv:response"]["serv:result"]) )
    response = xmltodict.parse(response)
    if str(response["serv:message"]["serv:header"]["serv:response"]["serv:result"]) == "SUCCESS":
        sendWebexMsg("EL evento ha sido creado exitosamente!!")
        meetingKey = response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:meetingkey"]
        #sendWebexMsg(str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:iCalendarURL"]["serv:attendee"]))
        #sendWebexMsg(str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:iCalendarURL"]["serv:host"]))
        #print(meetingKey)
        with open("app/getmeeting.xml") as file: 
            data = file.read()
        payload = data.format(meetingKey)
        response = requests.post( url, headers=headers, data = payload).text
        response = xmltodict.parse(response)
        #sendWebexMsg("Link para el Webex:")
        #sendWebexMsg(str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:meetingLink"]))
        sipURL = str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:sipURL"])
        print(sipURL)
        return sipURL

def createJWT(user_id,expirationTime,secret):
    key64 = base64.b64decode(secret)
    payload = {
    "sub": "Teleconsulta",
    "name": "Teleconsulta",
    "iss": user_id,
    "exp": expirationTime
    }
    headers= { "alg": "HS256","typ": "JWT" }
    encoded = str(jwt.encode(payload, key64, algorithm ='HS256', headers=headers).decode("utf-8"))
    #print(str(datetime.fromtimestamp(int(invitado.expirationTime.split(".")[0]))),str(datetime.fromtimestamp(int(datetime.utcnow().timestamp()))))
    return encoded

def sendSMS(contacto,token):
        text = "Servicio de TeleConsulta. Para iniciar la videollamada favor de ingresar a la siguiente direccion: https://teleconsulta.mx/widget?token=" + token 
        params = {'from': os.environ["sender"], 'text': text, 
                'to': contacto, 'api_key': os.environ["api_key"], 
                'api_secret': os.environ["api_secret"]}
        r = requests.post(os.environ["urlSMS"], params=params)
        if r.status_code == 200:
            responseBody = r.json()["messages"][0]
            print(r.json())
            if responseBody["status"] == "0":
                mensaje = "Mensaje enviado exitosamente al numero {}; queda un saldo de {}".format(responseBody["to"],
                                                                                      responseBody["remaining-balance"])
                sendWebexMsg(mensaje,os.environ["idRoomTodos"])
            else:
                mensaje = "Mensaje NO fue enviado; el detalle es: "+str(responseBody)
                sendWebexMsg(mensaje,os.environ["idRoomTodos"])     
        else:
            print(r.status_code)
            sendWebexMsg(r.status_code,os.environ["idRoomTodos"])


def generarWebex(listaNumeros=["5580663521"],correo="joarriag@cisco.com",nombre="teleconsulta"):
    actualTimePlusHR = str(datetime.utcnow().timestamp()+3600)
    sipURL = createWebexMeeting()
    for numero in listaNumeros:
        token = token_urlsafe(10)[:10]
        invitado = db.session.query(GuestUser).filter(GuestUser.expirationTime<=datetime.utcnow().timestamp()).first()
        invitado.indentficadorTemporal = token
        invitado.expirationTime = actualTimePlusHR
        invitado.correo = sipURL
        #print(invitado.username, str(datetime.fromtimestamp(invitado.expirationTime)))
        db.session.commit()
        sendSMS("+52"+numero,token)



def existeWebex(correo):
    return True

if __name__ == "__main__":
    #sendSMS("+5215580663521")
    #sendWebexMsg("prueba")