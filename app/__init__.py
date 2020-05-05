from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.ext.automap import automap_base


app = Flask(__name__)


app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://teleconsulta:C1sco123!@172.16.30.10/teleconsulta"
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
Agenda = Base.classes.Agenda


loginManager = LoginManager(app)
loginManager.login_view = "login"

from app import routes
