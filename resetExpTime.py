from app import db
from app import GuestUser
from app.funciones import createJWT
from datetime import datetime


for invitado in db.session.query(GuestUser).all() :
    invitado.expirationTime = 0
db.session.commit()

#createJWT()