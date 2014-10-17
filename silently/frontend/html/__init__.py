# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.lazyviews import LazyViews

bp = Blueprint('html', __name__)
views = LazyViews()
views.init_blueprint(bp, '.view')
views.add('/', 'home', methods=['GET'])
