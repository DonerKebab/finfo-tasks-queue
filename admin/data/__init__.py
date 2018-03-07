# -*- coding: utf-8 -*-
from functools import wraps
import sys

from flask import jsonify, current_app as app, abort, request

from .. import factory



def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    return app

