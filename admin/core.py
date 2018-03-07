from flask.ext.sqlalchemy import SQLAlchemy
from .search import ElasticSearch


#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

#: Elastic search instance
es = ElasticSearch()