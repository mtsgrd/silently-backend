# -*- coding: utf-8 -*-

from werkzeug.urls import url_decode


class HTTPMethodOverrideMiddleware(object):
    """Overrides HTTP Methods based on headers.

    Borrowed from Overholt's Flask skeleton.
    """

    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app, header_name=None,
                 querystring_param=None, allowed_methods=None):
        header_name = header_name or 'X-HTTP-METHOD-OVERRIDE'

        self.app = app
        self.header_name = 'HTTP_' + header_name.replace('-', '_')
        self.querystring_param = querystring_param or '__METHOD__'
        self.allowed_methods = frozenset(allowed_methods or
            ['GET', 'HEAD', 'POST', 'DELETE', 'PUT', 'PATCH', 'OPTIONS'])

    def _get_from_querystring(self, environ):
        if self.querystring_param in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            return args.get(self.querystring_param)
        return None

    def _get_method_override(self, environ):
        return environ.get(self.header_name, None) or \
               self._get_from_querystring(environ) or ''

    def __call__(self, environ, start_response):
        method = self._get_method_override(environ).upper()

        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method

        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'

        return self.app(environ, start_response)


class DispatcherMiddleware(object):
    """Basedon werkzeug routing. This optionally leaves PATH INFO unmodified."""

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}

    def __call__(self, environ, start_response):
        script = environ.get('PATH_INFO', '')
        path_info = ''
        preserve_path = False
        while '/' in script:
            if script in self.mounts:
                app = self.mounts[script]['app']
                preserve_path = self.mounts[script]['preserve_path']
                break
            items = script.split('/')
            script = '/'.join(items[:-1])
            path_info = '/%s%s' % (items[-1], path_info)
        else:
            app = self.mounts.get(script, self.app)
        if not preserve_path:
            original_script_name = environ.get('SCRIPT_NAME', '')
            environ['SCRIPT_NAME'] = original_script_name + script
            environ['PATH_INFO'] = path_info
        return app(environ, start_response)
