# -*- coding: utf-8 -*-

from .. import factory
from ..core import socketio
from flask import request, current_app
from flask_socketio import emit
from ..routing import socket_route
from flask_login import current_user
from .ordrin import get_restaurants, get_details

def create_app(static_url_path=None, settings_override=None):
    """Returns the Overholt API application instance"""

    app = factory.create_app(__name__, static_url_path=static_url_path,
            settings_override=settings_override)
    #app.register_blueprint([ordrin_bp])
    socketio.init_app(app)
    return app

@socket_route('connect')
def connect():
    current_app.logger.info('Connected as: %s', current_user.user_id)

@socketio.on('disconnect', namespace='/default')
def disconnect():
    current_app.logger.info('Disconnected!')

@socket_route('restaurant_list')
def list_restaurants(address):
    restaurants = get_restaurants(address)
    emit('restaurant_list', restaurants)
    #for restaurant in restaurants:
    #    details = get_details(restaurant['id'])
    #    emit('restaurant_details', details)
