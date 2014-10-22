# -*- coding: utf-8 -*-

from flask_script import Command, Manager, Option
from ..api import create_app
from ..users.models import UserForm

app = create_app()
manager = Manager(app)

@manager.command
@manager.option('-v', '--verbose', help='help me')
def hello_world(verbose):
    print "Hello World"
    if verbose:
        print "How are you?"

@manager.command
@manager.option('-u', '--username', help='Username')
@manager.option('-p', '--password', help='Plaintext password')
@manager.option('-e', '--email', help='User email address')
def create_user(username=None, password=None, email=None):
    user = UserForm()
    user.user_id.data = username
    user.email.data = email
    user.password = password
    user.validate()
    user.save()
    print user
