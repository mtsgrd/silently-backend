# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer
from silently import api, frontend
from silently.middleware import DispatcherMiddleware

api_app = api.create_app()
frontend_app = frontend.create_app(static_url_path='')
public = DispatcherMiddleware(
    frontend_app,
    {'/socket.io': {'app': api_app, 'preserve_path': True}})

if __name__ == "__main__":
    server = SocketIOServer(('', 5000), public, resource="socket.io").serve_forever()
