# -*- coding: utf-8 -*-

import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = 'cezCupwob6EmivVuwerd'
    LOCALE = 'vi_VN.utf8'
    CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    SECURITY_CONFIRMABLE = True

    ELASTICSEARCH_PORT = 9200 
    ELASTICSEARCH_HOST = 'localhost'
    ELASTICSEARCH_INDEX = 'api'

    SQLALCHEMY_DATABASE_URI = 'oracle://ipa:TEST123@10.26.53.10:1521/TESTDB'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ELASTICSEARCH_CONFIG_FILE = os.path.join(APP_ROOT, '..', 'admin/es_mapping.json')
    ES_INDEXER_STRICT_MODE = True
    BULK_MAX = 300

    config_data = ''
    with open(ELASTICSEARCH_CONFIG_FILE) as f:
        config_data = json.load(f)

    ELASTICSEARCH_INDEX_SETTINGS = config_data

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    from celery.schedules import crontab

    CELERYBEAT_SCHEDULE = {
        'index_effective-secinfo': {
            'task': 'admin.tasks.index_effective',
            'schedule': crontab(minute='*/1', hour='8-17', day_of_week='mon-fri'),  # Executes every minute from 8am-17pm from monday to friday
        }
    }
    CELERY_IMPORTS = ("admin.tasks",)
    
class DevelopmentConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                          'tests/data-test.sqlite')
    WTF_CSRF_ENABLED = False
    ADMIN_PASSWORD = u'pass'


class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
