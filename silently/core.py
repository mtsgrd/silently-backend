# -*- coding: utf-8 -*-

from flask_principal import Principal
from flask.globals import _app_ctx_stack
from flask_login import LoginManager
from flask_redis import Redis
from flask_security import Security
from flask_wtf.csrf import CsrfProtect
from flask_cache import Cache

from .redis_loop import SocketIoRedisLoop
from .smtphandler import EmailErrorHandler
from .flask_errors import ErrorHandler
from flask_socketio import SocketIO

from flask.ctx import AppContext
from functools import update_wrapper

from flask_mongoengine import MongoEngine


# Email when server errors out.
email_errors = EmailErrorHandler()

# Flask-Security extension instance.
security = Security()

# Error handler
error_handler = ErrorHandler()

# Cache.
cache = Cache()

# Redis general.
redis = Redis()

# Redis gevent loop for subscriptions.
redis_loop = SocketIoRedisLoop()

socketio = SocketIO()

# Login manager.
login_manager = LoginManager()

# Mongo engine
mongo_engine = MongoEngine()

#: Flask-WTF extension instance
csrf = CsrfProtect()

#: Principal manager intance
principals = Principal(use_sessions=False)

# TODO: These should be move elsewhere.
def copy_current_app_context(f):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('This decorator can only be used at local scopes '
            'when an app context is on the stack.  For instance within '
            'view functions.')
    appctx = AppContext(top.app)
    def wrapper(*args, **kwargs):
        with appctx:
            return f(*args, **kwargs)
    return update_wrapper(wrapper, f)
