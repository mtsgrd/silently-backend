# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length

# Maximum length of an email address is 256 characters.
# See http://goo.gl/Tk29yv for more information.
EMAIL_FIELD = TextField('Email', [Length(min=4, max=256)])

# Arbitrarily setting the maximum password length to the same as email.
PASSWORD_FIELD = PasswordField('Password', [Length(min=4, max=256)])

class LoginForm(Form):
    email = EMAIL_FIELD
    password = PASSWORD_FIELD

class RegisterForm(Form):
    email = EMAIL_FIELD
    password = PASSWORD_FIELD
    firstname = TextField('Firstname', [Length(min=1, max=60)])
    lastname = TextField('Lastname', [Length(min=1, max=60)])
