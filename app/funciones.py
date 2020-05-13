import requests, os, jwt, xmltodict

from app.models import User
from app import GuestUser, Agenda
from datetime import datetime
from app import db  
from secrets import token_urlsafe
import jwt 
import base64
import time,calendar

from dotenv import load_dotenv
load_dotenv()


def sendWebexMsg(texto,roomId=os.environ["idRoomYo"]):
    payload = {"text": str(texto),"roomId": roomId   }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ os.environ["botToken"]
    }
    requests.post( os.environ["urlWebextTeams"], headers=headers, json = payload )

def ourloggin(texto,mandarWebexMsg=False):
    print(texto)
    if mandarWebexMsg:
        sendWebexMsg(texto,os.environ["idRoomTodos"])

def createWebexMeeting(nombre,fecha,host="joarriag.iner@gmail.com"):
    with open("app/createMeetings.xml") as file: 
        data = file.read()
    url = "https://api.webex.com/WBXService/XMLService"
    payload = data.format(nombre,fecha,host)
    print(payload)
    headers = {
    'Content-Type': 'text/plain'
    }
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    resultado = str(response["serv:message"]["serv:header"]["serv:response"]["serv:result"])
    if resultado == "SUCCESS":
        ourloggin(resultado+" al crear se sesion de Webex meetings",True)
        meetingKey = response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:meetingkey"]
        with open("app/getmeeting.xml") as file: 
            data = file.read()
        payload = data.format(meetingKey)
        response = requests.post( url, headers=headers, data = payload).text
        response = xmltodict.parse(response)
        sipURL = str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:sipURL"])
        print("EL evento '"+nombre+"' con fecha "+fecha+" ha sido creado exitosamente!!\nCon la SipURL: "+ sipURL)
        return sipURL
    else:
        ourloggin(resultado+" al crear se sesion de Webex meetings",True)
        razon = str(response["serv:message"]["serv:header"]["serv:response"]["serv:reason"])
        ourloggin("La razon es: "+razon,True)

def hostJoined(meetingKey):
    with open("app/getmeeting.xml") as file: 
            data = file.read()
    payload = data.format(meetingKey)
    url = "https://api.webex.com/WBXService/XMLService"
    headers = { 'Content-Type': 'text/plain'}
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    #print(response)
    hostJoined = str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:hostJoined"])
    return hostJoined == "true"

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
    return encoded

def sendAgendaSMS(contactos=["5580663521"],fecha="fecha en pruebas",tipo="tipo de prueba"):
    texto = "Se ha agendado una video llamada de "+tipo+"con el INER, con fecha/hora "+str(fecha)+". Recibira por SMS el acceso 10 minutos antes de la fecha/hora programada. Se recomienda ampliamente conectarse a traves de una red tipo WiFi"
    for contacto in contactos:
        sendSMS("+52"+contacto,texto)

def sendWidgetSMS(contacto,token):
    texto = "Servicio de TeleConsulta INER. Para iniciar la videollamada favor de ingresar a la siguiente direccion: https://iner.teleconsulta.mx/widget?token=" + token 
    sendSMS("+52"+contacto,texto)
"""
def sendSMS(contacto,text):
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
            sendWebexMsg(text,os.environ["idRoomTodos"])
        else:
            mensaje = "Mensaje NO fue enviado; el detalle es: "+str(responseBody)
            sendWebexMsg(mensaje,os.environ["idRoomTodos"])     
    else:
            print(r.status_code)
            sendWebexMsg(r.status_code,os.environ["idRoomTodos"])
"""
def sendSMS(contacto,text):

    url = "https://api.twilio.com/2010-04-01/Accounts/ACc14eae52a15ea3cb0594390aedba3b92/Messages.json"

    payload = 'To={}&From=+16602274976&Body={}'.format(contacto,text)
    headers = {
    'Authorization': 'Basic QUNjMTRlYWU1MmExNWVhM2NiMDU5NDM5MGFlZGJhM2I5MjphNDFjYjgxMGFhNGIwNjMxZjhlZTA5YTIzNWMwMzE4Yg==',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post( url, headers=headers, data = payload).json()

    url = "https://api.twilio.com"+ response["uri"]

    headers = {
    'Authorization': 'Basic QUNjMTRlYWU1MmExNWVhM2NiMDU5NDM5MGFlZGJhM2I5MjphNDFjYjgxMGFhNGIwNjMxZjhlZTA5YTIzNWMwMzE4Yg==',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    time.sleep(2)
    response = requests.get( url, headers=headers).json()

    texto = "El mensaje: '{}' \nCon status de '{}' al numero {}".format(response["body"],response["status"],response["to"])
    ourloggin(texto,True)



def generarWebex(listaNumeros=["5580663521"],correo="joarriag@cisco.com",nombre="teleconsulta"):
    fecha=datetime.utcnow().timestamp()
    sendWebexMsg(datetime.fromtimestamp(int(fecha)-18000))
    timeForWebex = datetime.fromtimestamp(int(fecha)-18000).strftime("%m/%d/20%y %H:%M:00")
    actualTimePlusHR = str(datetime.utcnow().timestamp()+3600)
    invitados = db.session.query(GuestUser).filter(GuestUser.expirationTime<=datetime.utcnow().timestamp()).all()
    if len(listaNumeros) > len(invitados):
        print("no hay suficientes GuestUsers para la sesion")
        return False
    sipURL = createWebexMeeting(nombre,timeForWebex,host=correo)    
    for numero,invitado in zip(listaNumeros,invitados):
        token = token_urlsafe(10)[:10]
        invitado.indentficadorTemporal = token
        invitado.expirationTime = actualTimePlusHR
        invitado.correo = sipURL
        db.session.commit()
        sendWidgetSMS(numero,token)
    return True

def agendarWebex(listaNumeros=["5580663521"],correo="joarriag@cisco.com",nombre="teleconsulta",fecha=datetime.utcnow().timestamp()):
    sendWebexMsg(datetime.utcfromtimestamp(int(fecha)))
    timeForWebex = datetime.utcfromtimestamp(int(fecha)).strftime("%m/%d/20%y %H:%M:00")
    return  createWebexMeeting(nombre,timeForWebex,host=correo)    

def cronSMS():
    actualTimePlusHR = str(datetime.utcnow().timestamp()+3600)
    ahora, en20min = (datetime.utcnow().timestamp()-18000,datetime.utcnow().timestamp()-16800)
    print(ahora,en20min)
    eventos = db.session.query(Agenda).filter(Agenda.fecha_hora.between(ahora,en20min)).all()
    for evento in eventos:
        sendWebexMsg(datetime.fromtimestamp(int(evento.fecha_hora)))
        listaNumeros = evento.celulares.split(",")
        print(listaNumeros)
        invitados = db.session.query(GuestUser).filter(GuestUser.expirationTime<=datetime.utcnow().timestamp()).all()
        if len(listaNumeros) > len(invitados):
            print("no hay suficientes GuestUsers para la sesion")
            return False
        sipURL = evento.SIP   
        for numero,invitado in zip(listaNumeros,invitados):
            print(numero)
            token = token_urlsafe(10)[:10]
            invitado.indentficadorTemporal = token
            invitado.expirationTime = actualTimePlusHR
            invitado.correo = sipURL
            db.session.commit()
            sendWidgetSMS(numero,token)
    return "SMSs Sends para "+str(len(eventos))

def existeWebex(correo="joarriag.iner@gmail.com"):
    correoSplit = correo.split("@")
    print(correo)
    correoURL = correoSplit[0]+"%40"+correoSplit[1]
    url = "https://api.ciscospark.com/v1/people?email="
    headers = {
    'Authorization': 'Bearer ZDJiMGQzNjctYTg4YS00ZjE0LWEwM2EtYTdlM2NiOWIyNDI3OGIxNTYyNTEtYjAx_PF84_9778f473-87b3-4fc8-9af5-a7dcf09d40db'
    }
    response = requests.get( url+correoURL, headers=headers).json()
    try:
        for item in response["items"]:
            for email in item["emails"]:
                print(email)
                if email == correo:
                    return True
    except :
        return False



if __name__ == "__main__":
    sendSMS("+525580663521","texto de prueba")
    sendWebexMsg("prueba")
