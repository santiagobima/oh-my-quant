from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length 

class LoginForm(FlaskForm):
    username = StringField('Insert your username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Insert your password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
    