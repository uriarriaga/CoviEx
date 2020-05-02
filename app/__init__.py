from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.ext.automap import automap_base
# Quitar cirs antes de subir a git hub
#from flask_cors import CORS


app = Flask(__name__)
# Quitar cirs antes de subir a git hub
#CORS(app)

app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://sql9336570:pHjGFAlvei@sql9.freemysqlhosting.net/sql9336570"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://uli:Kr4k3n1808!@192.168.100.24/teleconsultax"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

Familiar = Base.classes.Familiar
User = Base.classes.User
Paciente = Base.classes.Paciente
GuestUser = Base.classes.GuestUser


loginManager = LoginManager(app)
loginManager.login_view = "login"

from app import routes