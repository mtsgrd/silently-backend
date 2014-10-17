# -*- coding: utf-8 -*-

import logging

from flask import Blueprint
from flask.ext.lazyviews import LazyViews

from ...core import cache
from ...core import security

bp = Blueprint('auth', __name__)
views = LazyViews()
views.init_blueprint(bp, '.view')
views.add('/auth/login', 'login', methods=['POST'])
views.add('/auth/logout', 'logout', methods=['GET'])
views.add('/auth/temp', 'temp_auth', methods=['GET'])
views.add('/auth/reset', 'ResetAuth', methods=['POST', 'PUT'])
