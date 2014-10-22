# -*- coding: utf-8 -*-

from flask_mongoengine import Document
from flask import json, Response

class JSONResponse(Response):
    """Normal response with JSON helpers."""

    def __init__(self, obj, **kwargs):
        body = ''
        if isinstance(obj, str):
            body = obj
        elif isinstance(obj, Document):
            body = obj.to_json()
        else:
            body = json.dumps(obj)
        kwargs.setdefault('content_type', 'application/json')
        super(JSONResponse, self).__init__(body, **kwargs)
