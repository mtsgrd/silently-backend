# -*- coding: utf-8 -*-

from ordrin import APIs, TEST

class Ordrin(APIs):

    def __init__(self):
        """Do nothing.

        We will only call the parent constructor once we have an app object.
        """

    def init_app(self, app, servers=TEST):
        api_key = app.config['ORDRIN_API_KEY']
        super(Ordrin, self).__init__(api_key, servers)
