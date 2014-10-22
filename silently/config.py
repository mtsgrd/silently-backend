# -*- coding: utf-8 -*-

import os
import logging

from datetime import timedelta

# Debug options.
DEBUG = True
TRAP_HTTP_EXCEPTIONS = False
DEBUG_TB_PROFILER_ENABLED = False
LOG_LEVEL = logging.DEBUG

# TODO: Should this key be set by an env variable?
SECRET_KEY = 'not_so_secret'

# Switch for using compiled JS in base template.
USE_COMPILED_JS = False

# API Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ORDRIN_API_KEY = os.getenv('ORDRIN_API_KEY')

# Redis
REDIS_URL = "redis://127.0.0.1:6379/0"

# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Session
SESSION_COOKIE_NAME = 'sil'
SESSION_PROTECTION = None
PERMANENT_SESSION_LIFETIME = timedelta(31)

# Flask-Cache
CACHE_ENABLED = True
CACHE_TYPE = 'redis'
CACHE_DEFAULT_TIMEOUT = 30 * 24 * 3600
CACHE_REDIS_DB = 0

# Flask-MongoEngine
MONGODB_DB = os.getenv('MONGO_DATABASE')
MONGODB_USERNAME = os.getenv('MONGO_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGODB_HOST = os.getenv('MONGO_HOST')
MONGODB_PORT = os.getenv('MONGO_PORT')

WTF_CSRF_ENABLED = False
WTF_CSRF_SSL_STRICT = False

# Email settings
SMTP_FROM = ''
SMTP_PORT = 465
SMTP_FROM = ''
SMTP_BUFFER_LENGTH = 1
SMTP_PASSWORD = ""
SMTP_SERVER = ""
SMTP_USERNAME = ""

ENABLE_ERROR_EMAIL = False
ERROR_EMAIL_SUBJECT = ''
ERROR_EMAIL_ADDRESS = ['']
