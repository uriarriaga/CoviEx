from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True
db = SQLAlchemy(app)
loginManager = LoginManager(app)
loginManager.login_view = "login"

from app import routes