# -*- coding: utf-8 -*-

from .. import factory, rooms
from ..core import socketio, redis, redis_loop
from flask import request, current_app
from flask.ext.socketio import emit
from routing import socket_route
from flask_login import current_user

def create_app(settings_override=None, register_blueprints=True):
    """Returns the Overholt API application instance"""

    app = factory.create_app(__name__, __path__, settings_override)
    #app.register_blueprint([imported_bp_name])
    socketio.init_app(app)
    redis.init_app(app)

    channel = app.config['REDIS_SOCKETIO_CHANNEL']
    redis_loop.init_app(app, redis=redis, socketio=socketio)
    redis_loop.subscribe(channel)
    redis_loop.spawn_loop()
    return app


@socket_route('connect')
def connect(self):
    current_app.logger.info('Connected as: %s', current_user.user_id)

@socket_route('disconnect')
def disconnect(self):
    current_app.logger.info('Disconnected!')
    if not current_user.is_anonymous():
        redis.publish(current_user.user_id, 'KILL')

@socket_route('join_room')
def join(self, room):
    rooms.join(room)

@socket_route('leave_room')
def leave(self, room):
    room = rooms.leave(room)
