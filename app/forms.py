from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username    = StringField('Usuario', validators=[DataRequired()])
    password    = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    #submit = SubmitField('Acceder')

class smsForm(FlaskForm):
    sms = StringField('Telefono', validators=[DataRequired()])
    #submit = SubmitField('Generar Consulta')


class userForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired()])
	password = StringField('Contraseña', validators=[DataRequired()])
	email    = StringField('Email', validators=[DataRequired()])
	admin    = BooleanField()
	ad       = BooleanField()
	im       = BooleanField()
	tv       = BooleanField()
	submit   = SubmitField('Agregar Usuario')


class capturesForm(FlaskForm):

	patient_name = StringField('nombre_paciente', validators=[DataRequired()])
	patient_celular = StringField('celular_paciente', validators=[DataRequired()])
	patient_email    = StringField('email_paciente', validators=[DataRequired()])

	familiar_1_name = StringField('familiar_1_name', validators=[DataRequired()])
	familiar_1_celular = StringField('familiar_1_celular', validators=[DataRequired()])
	familiar_1_email    = StringField('familiar_1_email', validators=[DataRequired()])

	familiar_2_name = StringField('familiar_2_name', validators=[DataRequired()])
	familiar_2_celular = StringField('familiar_2_celular', validators=[DataRequired()])
	familiar_2_email    = StringField('familiar_2_email', validators=[DataRequired()])

	familiar_3_name = StringField('familiar_3_name', validators=[DataRequired()])
	familiar_3_celular = StringField('familiar_3_celular', validators=[DataRequired()])
	familiar_3_email    = StringField('familiar_3_email', validators=[DataRequired()])

	submit   = SubmitField('Agregar Datos')



