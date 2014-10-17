# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired

from ...services import users as user_service

__all__ = ['ExtendedRegisterForm']


class LoginForm(Form):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')
    next = TextField('Next')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = user_service.get(self.username.data)
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

class ResetRequestForm(Form):
    username = TextField('Username', [DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        user = user_service.get(self.username.data)
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if user and not user.email:
            self.username.errors.append('User email address unknown.')
            return False

        self.user = user
        return True

class ResetAuthForm(Form):
    username = TextField('Username', [DataRequired()])
    token = TextField('Token', [DataRequired()])
    new_password = PasswordField('Password', [DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        user = user_service.get(self.username.data)
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if user and not user.email:
            self.username.errors.append('User email address unknown.')
            return False

        return True
