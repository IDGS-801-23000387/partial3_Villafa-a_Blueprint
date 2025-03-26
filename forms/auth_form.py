from wtforms import Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField,PasswordField,EmailField,BooleanField,SubmitField, IntegerField, RadioField, HiddenField
from wtforms import validators
    
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegistrationForm(FlaskForm):
    name= StringField('Nombre ', validators=[DataRequired(), Length(min=4, max=50)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField('Registrarse')
