from flask import current_app
from flask.ext.login import current_user
from ..core import redis
from ..helpers import get_usec_utc_timestamp
from flask.ext.socketio import emit, join_room, leave_room
import simplejson as json
from werkzeug.exceptions import BadRequest, Unauthorized

def emit_to_room(message=None, state=None, event=None,
        value=None, icon=None, animation_id=None, user_id=None):

    if not state:
        state = REMEMBER | PUBLIC 

    if user_id:
        room = 'user-' + user_id
    elif animation_id:
        room = 'animation-' + animation_id
    else:
        raise Exception('Either username or animation id has to be defined')


    channel = current_app.config['REDIS_SOCKETIO_CHANNEL']
    ts = get_usec_utc_timestamp()
    redis_message = {'room': room,
                     'event': event,
                     'message': message,
                     'state': state,
                     'icon': icon,
                     'ts': ts,
                     'value': value }
    redis.publish(channel, json.dumps(redis_message))
    redis.rpush('room-' + room, json.dumps(redis_message))

def join(room):
    if len(room.split('-')) != 2:
        raise BadRequest('Invalid room key')

    room_type, room_id = room.split('-')
    if room_type not in ('animation', 'user'):
        raise BadRequest('Invalid room type')
    if room_type == 'user' and room_id != current_user.user_id:
        raise Unauthorized('Room access denied.')
    join_room(room)
    current_app.logger.info('%s joined room: %s', current_user.user_id, room)

def leave(room):
    leave_room(room)
    current_app.logger.info('%s left room: %s', current_user.user_id, room)
