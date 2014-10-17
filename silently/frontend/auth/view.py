from datetime import datetime
from ...services import users as user_service
from flask import jsonify, request, Response, session
from flask.views import MethodView
from flask.ext.login import current_user
from flask.ext.login import logout_user
from flask.ext.login import login_user
from .forms import LoginForm, ResetRequestForm, ResetAuthForm
from ...cookies import SilentlyCookie
from ...helpers import get_random_base_62_string, get_utc_timestamp
import simplejson as json

from ...async import sendmail
from werkzeug.exceptions import BadRequest, ServiceUnavailable


from flask import current_app
import uuid

def logout():
    """This is reserved for logout requests."""
    logout_user()
    return Response(status=200)


def login():
    """Login."""
    form = LoginForm()
    transferred_assets = []
    if form.validate_on_submit():
        user = user_service.get(request.form['username'])
        if current_user.temporary:
            transferred_assets = animation_service.transfer_ownerships(
                current_user.user_id, user.user_id)
        login_user(user)
        return jsonify(user.to_json(), transfers=transferred_assets)
    else:
        return Response(json.dumps(form.errors), status=401)


def temp_auth():
    glc = SilentlyCookie(request.cookies.get('glc', ''))
    user_id = str(uuid.uuid4())
    user = user_service.new(user_id=user_id, username=user_id)
    user.temporary = True
    user.frame_limit = current_app.config['UNREGISTERED_FRAME_LIMIT']
    login_user(user)
    session['user'] = user
    return jsonify(user.to_json())


def put(user_id):
    # update a single user
    pass

class ResetAuth(MethodView):

    _DOMAIN = 'www.silently.com'

    def post(self):
        form = ResetRequestForm()
        if form.validate_on_submit():
            reset_token = get_random_base_62_string(length=32)
            reset_expiry = get_utc_timestamp() + 30 * 60
            user = form.user
            user.reset_token = reset_token
            user.reset_expiry = reset_expiry
            user.save()
            user_service.invalidate(user.user_id)
            email_template = """
            <h2>Silently account recovery request</h2>
            <p>We have received an account recovery request for your account.
            Please click
            <a href='https://%s/recovery?username=%s&token=%s'>here</a>.</p>
            <p>If you did not make the request then please let us know by
            writing to info@silently.com</p><p><i>- The Silently team</i></p>
            """
            email_message = email_template % (self._DOMAIN, form.username.data,
                                              reset_token)
            try:
              current_app.logger.debug('Trying to send email to %s.',
                      user.email)
              sendmail.delay(to_addr=user.email,
                             from_name='Silently Account Recovery',
                             from_address='noreply@silently.com',
                             subject='Account Recovery',
                             body=email_message)
              return Response(status=200)
            except:
              current_app.logger.debug('Failed')
              raise ServiceUnavailable('Error sending email.')
            current_app.logger.debug('Password reset requested for %s.',
                                     user.user_id)
        return BadRequest(json.dumps(form.errors))

    def put(self):
        form = ResetAuthForm()
        if form.validate_on_submit():
            user_id = form.username.data.lower()
            user = user_service.get(user_id)
            token = form.token.data
            new_password = form.new_password.data
            if user and user.reset_token and user.reset_token == token:
                token = user.reset_token
                expiry = datetime.fromtimestamp(int(user.reset_expiry))
                now = datetime.fromtimestamp(get_utc_timestamp())
                if now < expiry:
                    user.set_password(new_password)
                    user.reset_token = None
                    user.save()
                    user_service.invalidate(user.user_id)
                    login_user(user)
                    return jsonify(user.to_json())
                return Response('Reset token expired.', status=409)
            return Response('User has no reset token.', status=409)
        return Response(json.dumps(form.errors), status=400)
