# -*- coding: utf-8 -*-

from flask_security import UserMixin, RoleMixin
from passlib.hash import sha256_crypt

from ..core import mongo_engine as db
from flask_security import AnonymousUser
from flask import current_app
import datetime


class Role(RoleMixin, db.Document):
    user_id = db.StringField(max_length=16)
    name = db.StringField()

    def __repr__(self):
        return "<Role '%s'>" % (self.name)


class User(UserMixin, db.Document):

    user_id = db.StringField(max_length=16)
    name = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.now)
    email = db.StringField(max_length=60)
    password = db.StringField()
    active = db.BooleanField()


    def __repr__(self):
        return "<User '%s'>" % (self.user_id,)


    def check_password(self, password):
        match = sha256_crypt.verify(password, self.password)
        current_app.logger.debug('Password match for %s against %s: %s',
                                 password, self.password, match)
        return match

    def set_password(self, password):
        self.password = sha256_crypt.encrypt(password)
        current_app.logger.debug('Set password for %s: %s',
                                 self.user_id, self.password)

    def is_active(self):
        self.active

    @property
    def id(self):
        # Why does this have to be named `id`?
        return self.username


class AnonymousUser(AnonymousUser):
    """Keeping anonymous user feature parity."""

    def is_admin(self):
        return False

    def to_json(self):
        return {}

    @property
    def user_id(self):
        return self.get_id()

    def is_anonymous(self):
        return True

    @property
    def temporary(self):
        return False

    @property
    def username(self):
        return ''
