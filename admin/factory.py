# -*- coding: utf-8 -*-
"""
    admin.factory
    ~~~~~~~~~~~~~

    admin factory module
"""

import os
from flask import Flask, current_app
import locale
from celery import Celery

from .config import config
from .core import db, es



def create_app(package_name, package_path, settings_override=None, register_security_blueprint=True):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the CBP Admin platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    es.init_app(app)
    
    return app


def create_celery_app(app=None):
    app = app or create_app('admin', os.path.dirname(__file__))
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

