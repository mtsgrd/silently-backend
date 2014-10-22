from flask import current_app, copy_current_request_context
from flask_socketio import emit
from functools import wraps
from .core import socketio
import gevent

def socket_route(message, **kwargs):
    """Socket event listener.

    This decorator is used for customizing handling of incoming messages on
    websockets.

    Args:
        message (string): The message type to listen for.

    """
    def decorator(f):
        # Wraps preservers function name and docstring of the decorated
        # function.
        @wraps(f)

        # Leaving the namespace empty does not work in gevent-socketio so we
        # set a default.
        @socketio.on(message, namespace='/default', **kwargs)
        def inner(*args, **kwargs):

            # Spawn a greenlet so the main thread can continue looping.
            @socket_thread
            def execute_task():
                try:
                    # Websockets don't automatically log anything so we use
                    # this decorator to keep track of what's executing.
                    current_app.logger.info('Socket.io - %s', message)
                    f(*args, **kwargs)
                except Exception as err:
                    # Send HTTP errors to the client if status code available.
                    if hasattr(err, 'code'):
                        error = {'name': e.name,
                                 'message': e.message,
                                 'description': e.description,
                                 'code': e.code}
                        emit(message, error)
                    else:
                        current_app.log_exception(err)
            return execute_task()
        return f
    return decorator

def socket_thread(f):
    """Decorator to wrap a function in a greenlet.

    It's necessary to copy the request context using the convenience method
    provided by the flask library.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        return gevent.spawn(copy_current_request_context(f), *args, **kwargs)

    # Wraps preservers function name and docstring of the decorated function.
    return inner
