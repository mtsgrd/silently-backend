# -*- coding: utf-8 -*-

import os
from os import path

import jinja2
from celery import Celery
from celery.utils import LOG_LEVELS
from flask_kvsession import KVSessionExtension
from flask_security.datastore import MongoEngineUserDatastore
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter

import wtforms_json
from simplekv.memory.redisstore import RedisStore

from .core import (csrf, login_manager, principals,
                   security, redis, email_errors, mongo_engine,
                   cache, error_handler, ordrin_api)
from .silently_flask import SilentlyFlask
from .middleware import HTTPMethodOverrideMiddleware
from .users.models import AnonymousUser, User, Role
from . import signals

UUID_REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def create_app(package_name, static_url_path=None, settings_override=None):
    """Creates a configured Flask instance.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    """


    app = SilentlyFlask(package_name, instance_relative_config=True,
                static_url_path=static_url_path)

    # Load the config file.
    # TODO: This could be refactored to be more dynamic.
    app.config.from_object('silently.config')

    # Override config where specified.
    if settings_override:
        app.config.update(**settings_override)

    # Let's use a regex converter for more power.
    app.url_map.converters['regex'] = RegexConverter

    loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(path.join(path.dirname(__file__), 'templates'))
    ])
    app.jinja_loader = loader

    # TODO: These error handler inits must be refactored.
    security.init_app(app, MongoEngineUserDatastore(None, User, Role),
                      register_blueprint=False)

    # Initialize flask_redis.
    redis.init_app(app)

    # Initialize flask_cache for memoize functionality.
    cache.init_app(app)

    # Initialize mongo_engine for MongoDB ORM like features.
    mongo_engine.init_app(app)

    # Use Redis as the simple key value store for sessions.
    store = RedisStore(redis)
    KVSessionExtension().init_app(app, session_kvstore=store)

    # Initialize flask_login manager.
    login_manager.init_app(app)

    # Set a custom anonymous object.
    login_manager.anonymous_user = AnonymousUser

    # Initialize flask_principal for resource access control.
    principals.init_app(app)

    # There are lots of legacy proxy servers in the wild that do not allow
    # certain methods like PATCH. To overcome this it is necessary to specify
    # the method in a header, and use middleware to transform the request
    # before it is routed.
    app.wsgi_app = ProxyFix(HTTPMethodOverrideMiddleware(app.wsgi_app))

    # Send emails in case of server errors. This handler is used with calls
    # to flask.log_exception.
    if app.config['ENABLE_ERROR_EMAIL']:
        email_errors.init_app(app)

    # Allow CSRF tokens to be transmitted in JSON data.
    wtforms_json.init()

    # Init CSRF helper.
    csrf.init_app(app)

    # Initialize signal handlers.
    signals.init_app(app)

    # Initialize Error Handler
    error_handler.init_app(app)

    # Initialize the ordrin API.
    ordrin_api.init_app(app)

    return app

def create_celery_app(app=None, settings_override=None):
    """Creates a celery app to perform asynchronous jobs.

    Params:
        app: A Flask app.
        settings_override: Override settings from config file.
    """
    app = app or create_app('silently_celery', os.path.dirname(__file__),
            settings_override)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    if app.debug == True:
        #Disable while image data is written to the log.
        celery.conf.CELERYD_LOG_LEVEL = LOG_LEVELS['DEBUG']

    class ContextTask(celery.Task):
        """Add Flask app context awareness."""
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery.Task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
