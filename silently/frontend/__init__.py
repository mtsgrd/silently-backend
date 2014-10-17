# -*- coding: utf-8 -*-

from ..helpers import is_mobile
from xml.sax.saxutils import escape as xml_escape
import simplejson as json
from .. import factory
from .html import bp as html_bp

#from .html import bp as html_bp
#from .auth import bp as auth_bp

def xml(data):
    if data:
        return xml_escape(data)
    else:
        return ''

def safe_json(data):
    return str(json.dumps(data,
                      ensure_ascii=False).replace('\\', '\\\\'))

def create_app(settings_override=None,
               static_url_path=None):
    """Returns the Overholt API application instance"""

    app = factory.create_app(__name__, settings_override,
         static_url_path=static_url_path)

    app.register_blueprint(html_bp)
    #app.register_blueprint(auth_bp)

    # Register custom error handlers
    #toolbar = DebugToolbarExtension(app)

    @app.context_processor
    def template_data():
        return dict(is_mobile = is_mobile())
    app.jinja_env.filters['xml'] = xml
    app.jinja_env.filters['safe_json'] = safe_json
    return app
