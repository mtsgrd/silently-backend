from .core import login_manager, principals
from flask_principal import (identity_changed, identity_loaded, UserNeed,
                                 RoleNeed, AnonymousIdentity, Identity)
from flask import request
from flask_security  import current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """Flask security loads the user before flask login. See the flask security
    AWSDataStore.
    """
    return None #users.get(user_id)

@principals.identity_loader
def load_identity_from_weird_usecase():
    if current_user.is_anonymous():
        return AnonymousIdentity()
    else:
        return Identity(current_user.user_id)

def init_app(app):
    """Initializing app specifc signal handlers."""

    # TODO: Is this daisy chaining correct?
    @identity_loaded.connect_via(app)
    @identity_changed.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(identity.user, 'user_id'):
            user_need = UserNeed(current_user.user_id)
            identity.provides.add(user_need)

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(identity.user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.after_request
    def _nocache(response):
        """Appends no-cache headers just before response is transmitted.

        This should be rewritten to support init_app like functionality
        """
        if hasattr(request, 'glc'):
            response.headers['Last-Modified'] = datetime.now()
            response.headers['Cache-Control'] = \
                    'no-store, no-cache, must-revalidate, post-check=0, ' + \
                    'pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'

        return response

