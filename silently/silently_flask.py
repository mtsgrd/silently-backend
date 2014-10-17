# -*- coding: utf-8 -*-

import logging
from logging import StreamHandler
from flask import Flask, request
from flask_security import current_user

class SilentlyFlask(Flask):
    """Overriding the Flask app.

    All default behavior modifications to Flask should go here.
    """

    def log_exception(self, exc_info):
        """Custom handler for logging an exception.
        """
        error_msg = ''

        error_items = [('Request', request.method + ' ' + request.path),
                       ('IP', request.remote_addr),
                       ('User agent', request.user_agent.string),
                       ('User', current_user),
                       ('JSON', request.get_json())]

        for key, value in error_items:
            error_msg += '%s: %s\n' % (key, str(value).rjust(24-len(key)))

        client_side_items = request.values.items()
        for key, value in client_side_items:
            error_msg += '%s: %s\n' % (key, str(value).rjust(24-len(key)))

        for key, value in request.headers.items():
            error_msg += '%s: %s\n' % (key, str(value).rjust(20))
        self.logger.error(error_msg, exc_info=exc_info)


    @property
    def logger(self):
        """Custom logger for nicer log format.

        Not sure why this was needed, but I remember being dissatisfied with
        the built in logging behavior of flask.
        """
        if self._logger:
            return self._logger
        else:
            logger = logging.getLogger(self.logger_name)
            stream_handler = StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(filename)s - ' +
                    '%(name)s:%(lineno)d - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            logger.setLevel(self.config['LOG_LEVEL'])
            logger.addHandler(stream_handler)
            self._logger = logger
            return logger


