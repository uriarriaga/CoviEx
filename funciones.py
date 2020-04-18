import requests

def sendWebexMsg(texto):
    url = "https://api.ciscospark.com/v1/messages"
    idRoomTodos = "Y2lzY29zcGFyazovL3VzL1JPT00vNjFiYTM4ZDAtNzQzZS0xMWVhLTg1YzMtODM5MjNiY2UxMjFm"
    idRoomYo = "Y2lzY29zcGFyazovL3VzL1JPT00vMTRkMzU4OGQtNzBkNi0zZDRkLWFkMDMtNmEzZGE2NjNjMjUw"
    payload = {"text": texto,"roomId": idRoomTodos}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ZTNjZjBiZTMtNjhmOC00ODJkLTg3MzAtMjg0MTAxNDBlNWY4MDljYTkwMmQtNGY0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
    }
    requests.post( url, headers=headers, json = payload)