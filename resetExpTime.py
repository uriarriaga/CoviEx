from app import db
from app import GuestUser
from app.funciones import createJWT
from datetime import datetime

db.session.query(GuestUser).all()[0].expirationTime = 0
db.session.query(GuestUser).all()[1].expirationTime = 0
db.session.commit()

#createJWT()