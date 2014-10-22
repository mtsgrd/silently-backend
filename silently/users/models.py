# -*- coding: utf-8 -*-

import datetime

from flask import current_app
from flask_security import AnonymousUser, UserMixin, RoleMixin
from flask_mongoengine.wtf import model_form
from ..core import mongo_engine as db


class Role(RoleMixin, db.EmbeddedDocument):
    """MongoDB role model for managing resource access."""
    user_id = db.StringField(max_length=16)
    name = db.StringField()

    def __repr__(self):
        return "<Role '%s'>" % (self.name)


class User(db.Document, UserMixin):
    """MongoDB user model."""

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

# WTForms enables some convenient functionality with forms.
UserForm = model_form(User)


class AnonymousUser(AnonymousUser):
    """Anonymous user model.

    This model should be used for extending functionality on unauthenticated
    users.
    """

    def is_admin(self):
        return False

    def to_json(self):
        return {}

    def is_anonymous(self):
        return True
