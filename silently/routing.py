from flask import current_app, copy_current_request_context
from flask_socketio import emit
from functools import wraps
from .core import socketio
import gevent

def socket_route(message, **options):
    """Socket event listener.

    Args:
        message (string): The message type to listen for.

    """
    def decorator(f):
        # Wraps preservers function name and docstring of the decorated
        # function.
        @wraps(f)

        # Namespace default to avoid the hassle.
        @socketio.on(message, namespace='/default', **options)
        def inner(*args, **kwargs):
            @socket_thread
            def execute_task():
                try:
                    current_app.logger.info('Socket.io - %s', message)
                    f(*args, **kwargs)
                except Exception as err:
                    if hasattr(err, 'code'):
                        # Send HTTP errors to the client.
                        error = {'name': e.name,
                                 'message': e.message,
                                 'description': e.description,
                                 'code': e.code}
                        emit(message, error)
                    else:
                        # Otherwise we'll probably want to be notified.
                        current_app.log_exception(err)
            return execute_task()
        return f
    return decorator

def socket_thread(f):
    """Decorator to wrap a function in a greenlet.

    It's necessary to copy the request context using the convenience method
    provided by the flask library.
    """
    def inner(*args, **kwargs):
        return gevent.spawn(copy_current_request_context(f), *args, **kwargs)
    return inner
