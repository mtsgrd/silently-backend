from flask import current_app
import simplejson as json
import gevent
from traceback import print_exc

class SocketIoRedisLoop(object):
    """Object to sit and wait for Redis to say something."""

    jobs = []

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app, redis=None, socketio=None):
        self.app = app
        self.redis = redis
        self.pubsub = redis.pubsub()
        self.socketio = socketio

    def subscribe(self, channels):
        self.pubsub.subscribe(channels)
        self.app.logger.info('Listening to Redis channels: %s', channels)

    def spawn_loop(self):
        job = gevent.spawn(self.redis_loop)
        self.jobs.append(job)
        return job

    def emit(self, data, fresh=True):
        room = data.get('room')
        event = data.get('event')
        value = data.get('value')
        room_key = self.room_key(room)

        if not room:
            return
        self.socketio.emit('room_message', data, namespace='/default',
                room=room)

    def room_key(self, room):
        return 'room-%s' % room

    def redis_loop(self):
        for item in self.pubsub.listen():
            self.app.logger.debug('Redis message received: %s', item)
            try:
                data = json.loads(item['data'])
                data['channel'] = item['channel']
                self.emit(data)
            except TypeError:
                # Non JSON data.
                pass
            except Exception as e:
                print_exc()
