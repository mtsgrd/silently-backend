from flask import current_app
from flask.ext.socketio import emit
from ..core import socketio
import gevent

def socket_route(message, **options):
    def decorator(f):
        f.route_name = message
        @socketio.on(message, namespace='/default')
        def inner(data=None):
            f.socket_request = True
            @socket_thread
            def execute_task():
                try:
                    current_app.logger.info('Socket.io - %s', message)
                    current_app.preprocess_request()
                    rv = f(f, *data)
                    emit(message, rv)
                    return rv
                except Exception as e:
                    if hasattr(e, 'code'):
                        # If the exception has a status code then send it to
                        # client.
                        error = {'name': e.name,
                                 'message': e.message,
                                 'description': e.description,
                                 'code': e.code}
                        if hasattr(e, 'payload'):
                            error['payload'] = e.payload
                        emit(message, error)
                    else:
                        # Otherwise we'll probably want to be notified.
                        current_app.log_exception(e)
            return execute_task()
        return f
    return decorator

def socket_thread(f):
    def inner(*args, **kwargs):
        return gevent.spawn(copy_current_request_context(f), *args, **kwargs)
    return inner

