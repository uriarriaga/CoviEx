import requests, os, jwt
from dotenv import load_dotenv
load_dotenv()


def sendWebexMsg(texto,roomId=os.environ["idRoomYo"]):
    payload = {"text": texto,"roomId": roomId   }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ os.environ["botToken"]
    }
    requests.post( os.environ["urlWebextTeams"], headers=headers, json = payload )



def sendSMS(contacto):
        text = "Servicio de TeleConsulta. Para iniciar la videollamada favor de ingresar a la siguiente direccion: https://teleconsulta.mx/widget"
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

if __name__ == "__main__":
    sendSMS("+5215580663521")
    #sendWebexMsg("prueba")