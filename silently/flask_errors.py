from flask import jsonify, request, render_template
import traceback

def handle_exception(err):
    """Handles exceptions.

    If the exception raised doesn't have a code attribute then we re-raise
    it to allow Flask's log_exception method to deal with it.
    """
    if request.is_xhr:
        return jsonify(dict(error=err.description)), err.code
    else:
        return render_template('%s_error.html' % err.code,
                err_stack=traceback.extract_stack(),
                err_message=err.description
                ), err.code

class ErrorHandler(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.errorhandler(400)(handle_exception)
        app.errorhandler(401)(handle_exception)
        app.errorhandler(403)(handle_exception)
        app.errorhandler(404)(handle_exception)
        app.errorhandler(500)(handle_exception)
        app.errorhandler(502)(handle_exception)
        app.errorhandler(503)(handle_exception)

