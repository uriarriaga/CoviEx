from datetime import datetime
from app import db,loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):

    __tablename__='User'
    id                   = db.Column(db.Integer,primary_key=True)
    username             = db.Column(db.String(20),unique = True, nullable = False)
    email                = db.Column(db.String(120),unique = True, nullable = False)
    password             = db.Column(db.String(60), nullable = False)
    admin                = db.Column(db.Boolean, nullable = False)
    atencionDomiciliaria = db.Column(db.Boolean, nullable = False)
    informeMedico        = db.Column(db.Boolean, nullable = False)
    teleVisita           = db.Column(db.Boolean, nullable = False)

    def __init__(self,username,email,password,admin,atencionDomiciliaria,informeMedico,teleVisita):
        self.username = username
        self.email = email
        self.password =password
        self.admin = admin
        self.atencionDomiciliaria = atencionDomiciliaria
        self.informeMedico= informeMedico
        self.teleVisita = teleVisita

    def __repr__(self):
        return(f"User('{self.username}','{self.email}')")

class GuestUser(db.Model):
    id                   = db.Column(db.Integer,    primary_key=True)
    username             = db.Column(db.String(20), unique = True, nullable = False)
    user_id              = db.Column(db.String(120),unique = True, nullable = False)
    secret               = db.Column(db.String(60), nullable = False)
    expirationTime       = db.Column(db.Integer,    default = datetime.utcnow().timestamp())
    

    def __repr__(self):
        return(f"GuestUser('{self.username}','{self.expirationTime}')")


