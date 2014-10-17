# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
from flask_script import Manager

from silently.api import create_app
from silently.manage import HelloWorld

app = create_app()
manager = Manager(app)
manager.add_command('hello_world', HelloWorld())

@manager.command
def runserver():
    app.logger.debug("Trying to run server")
    socket_server = SocketIOServer(('', 5000), app, resource="socket.io",
                                   policy_server=False)
    socket_server.start()
    try:
        stopper.wait()
    except KeyboardInterrupt:
        print

if __name__ == "__main__":
    manager.run()
