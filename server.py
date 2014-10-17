# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    overholt wsgi module
"""

from werkzeug.serving import run_simple
from socketio.server import SocketIOServer

from silently import api, frontend
from silently.middleware import DispatcherMiddleware
import logging
import flask


api_app = api.create_app()
frontend_app = frontend.create_app(static_url_path='')
public = DispatcherMiddleware(
    frontend_app,
    {'/socket.io': {'app': api_app, 'preserve_path': True},
     '/api': {'app': api_app, 'preserve_path': False}})

if __name__ == "__main__":
    SocketIOServer(('', 5000), public, resource="socket.io").serve_forever()
