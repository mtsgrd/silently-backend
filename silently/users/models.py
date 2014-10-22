# -*- coding: utf-8 -*-

from flask_security import UserMixin, RoleMixin

from ..core import mongo_engine as db
from flask_mongoengine.wtf import model_form
from flask_security import AnonymousUser
from flask import current_app
import datetime


class Role(RoleMixin, db.EmbeddedDocument):
    user_id = db.StringField(max_length=16)
    name = db.StringField()

    def __repr__(self):
        return "<Role '%s'>" % (self.name)


class User(db.Document, UserMixin):

    meta = { 'collection': 'users',
             'allow_inheritance': True }

    email = db.StringField(required=True)
    password = db.StringField(required=True)
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now)
    roles = db.ListField(db.EmbeddedDocumentField(Role))

    @property
    def active(self):
        return True

    def __repr__(self):
        return "<User '%s'>" % (self.email,)

UserForm = model_form(User)


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
