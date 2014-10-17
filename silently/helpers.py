# -*- coding: utf-8 -*-

import calendar
import dateutil
import dateutil.parser
import httpagentparser
import importlib
import pkgutil
import random
import time

from datetime import datetime
from flask import Blueprint, request


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
USER_DOMAIN_COUNT = 10

def get_random_base_62_string(length=7):
    return ''.join(random.choice(ALPHABET) for x in range(length))


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        print 'Trying to import %s.%s from %s' % (package_name,
                name, package_path)
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


def register_view(bp, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None},
            view_func=view_func, methods=['GET',])
    bp.add_url_rule(url, view_func=view_func, methods=['POST',])
    bp.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
            methods=['GET', 'PUT', 'DELETE'])



def get_utc_timestamp():
    """Returns the current time in seconds.

    :return: current epoch.
    """
    return int(time.time())

def get_msec_utc_timestamp():
    """Returns the current time in seconds.

    :return: current epoch.
    """
    return int(time.time() * 1000)

def get_usec_utc_timestamp():
    """Returns the current time in microseconds.

    :return: current epoch.
    """
    return int((time.time()) * 1000000)

def date_to_usec(dt):
    return int(calendar.timegm(dt.timetuple()) * 1000000)

def date_str_to_usec(dt_str):
    dt = dateutil.parser.parse(dt_str)
    return int(calendar.timegm(dt.timetuple()) * 1000000)

def date_to_ts(dt):
    return int(calendar.timegm(dt.timetuple()))

def date_to_msec(dt):
    return int(calendar.timegm(dt.timetuple()) * 1000)

def ms_to_date_str(ms):
    return datetime.fromtimestamp(int(ms)/1000.0).isoformat()

def is_mobile():
    useragent = httpagentparser.detect(request.user_agent.string)
    if useragent.get('dist', {}).get('name', '').lower() in ['ipad', 'iphone',
            'android']:
        return True
    else:
        return False
