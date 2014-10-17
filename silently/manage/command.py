# -*- coding: utf-8 -*-

from flask.ext.script import Command, prompt
from ..services import users as user_service
from ..helpers import manual_login
from flask import current_app
from flask.ext.principal import identity_changed, Identity

class SilentlyCommand(Command):
    def run(self, impersonate=None, *args, **kwargs):
        script_user = current_app.config['SCRIPT_USER']
        if not script_user:
            login()
        else:
            login(user_id=script_user)


def login(user_id=None):
    if not user_id:
        user_id = prompt('Impersonate')
    try:
        user = user_service.get(user_id)
        manual_login(user)
        current_app.logger.info('Impersonating %s', user_id)
        identity_changed.send(current_app._get_current_object(),
                identity=Identity(user_id))
    except:
        current_app.logger.info('Failed to impersonate %s', user_id)
        raise
