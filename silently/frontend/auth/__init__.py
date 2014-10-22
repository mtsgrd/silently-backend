# -*- coding: utf-8 -*-

from hashlib import sha256
from flask import Blueprint, Response, request

from ...core import cache, security, ordrin_api
from .forms import LoginForm, RegisterForm
from flask import jsonify, current_app
from flask_login import login_user, logout_user
from flask_principal import identity_changed, Identity, UserNeed
from ...users.models import User
from ...json_util import JSONResponse

bp = Blueprint('auth', __name__)

def login(user):
    """Logs a user in.

    Every login should be followed by a signal that the a change in identity
    such that roles can be updated.

    Args:
        user (silently.users.models.User): A user object.
    """
    login_user(user)
    identity_changed.send(current_app._get_current_object(),
            identity=Identity(user.email))

@bp.route('/auth/login', methods=['POST'])
def sign_in():
    """Gets account info for ordrin customer.

    This is equivalent to user authentication since an incorrect password
    will throw an exception.

    Returns:
        The user account info as a dict.

    Raises:
        Whatever the API raises.
    """
    form = LoginForm()
    if not form.validate():
        return JSONResponse({'errors': form.errors})

    email = request.form.get('email')
    password = request.form.get('password')
    data = ordrin_api.get_account_info(email, password)
    user = User(email=data['em'], password=data['pw'],
            firstname=data['first_name'], lastname=data['last_name'])
    user.save()
    login(user)
    return JSONResponse(user)

@bp.route('/auth/register', methods=['POST'])
def register():
    """Registers a new user with ordrin.

    If account creation is successful then this responds with a
    secure authentication token.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    user = User(email=email, password=password, firstname=firstname,
            lastname=lastname)
    form = RegisterForm(request.form, user)

    if form.validate_on_submit():
        # Account creation is succesful unless the following function raises
        # an exception. To stay on the safe side, we assert _err == 0.
        res = ordrin_api.create_account(email, password, firstname,
            lastname)
        assert not res['_err']
        # TODO: Refactor password hashing. The ordr.in python library should
        # probably be refactored so it can accept already hashed passwords.
        user.password = sha256(password).hexdigest()
        user.save()
        login(user)
        return JSONResponse(user)
    else:
        return JSONResponse({'errors': form.errors})

@bp.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    """This is reserved for logout requests."""
    logout_user()
    return Response(status=200)
