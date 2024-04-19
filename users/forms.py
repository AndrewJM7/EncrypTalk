
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
import re
from flask_wtf import RecaptchaField

# A function that excludes some special characters
def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")

# A regex function for password validation
def validate_password(form, password):
    p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W+)")
    if not p.match(password.data):
        raise ValidationError("Must contain at least 1 digit, 1 lowercase character, 1 uppercase character and 1 special character ")
        
class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), character_check])
    lastname = StringField(validators=[DataRequired(), character_check])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), validate_password])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both passwords must be equal')])

    submit = SubmitField()
    
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    
    submit = SubmitField()