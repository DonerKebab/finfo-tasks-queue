# # -*- coding: utf-8 -*-
# """
#     admin.tasks
#     ~~~~~~~~~~

#     admin tasks module
# """
from flask import current_app
from celery.utils.log import get_task_logger
import json
import datetime

from .factory import create_celery_app
from .data.db_indexing import index_effective_secinfo

celery = create_celery_app(current_app)
logger = get_task_logger(__name__)


@celery.task(bind=True)
def index_effective(self):
	index_effective_secinfo()





