from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    #submit = SubmitField('Acceder')

class smsForm(FlaskForm):
    sms = StringField('Telefono', validators=[DataRequired()])
    #submit = SubmitField('Generar Consulta')


class userForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired()])
	password = StringField('Contraseña', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	admin = BooleanField(validators=[DataRequired()])
	ad = BooleanField(validators=[DataRequired()])
	im = BooleanField(validators=[DataRequired()])
	tv = BooleanField(validators=[DataRequired()])
	submit = SubmitField('Agregar Usuario')







