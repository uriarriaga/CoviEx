from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.ext.automap import automap_base

import os


app = Flask(__name__)

app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["URL_DB"]
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
