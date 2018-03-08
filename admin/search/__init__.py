# -*- coding: utf-8 -*-
from flask import current_app

from elasticsearch import Elasticsearch as PyElasticSearch, RequestsHttpConnection

from .utils import get_config

import json


class ElasticSearch(object):
  
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        port = get_config(app)['PORT']
        host = get_config(app)['HOST']

        try:
            # connect to ElasticSearch
            app.extensions['elasticsearch'] = PyElasticSearch(host, timeout=60, port=port,
                                                              connection_class=RequestsHttpConnection)
            app.extensions['elasticsearch'].cluster.health()

            # check there is new type in es_mapping.json file
            self.init_index(app)
        
        except Exception as e:
           print('Can not connect to Elasticsearch')

    def init_index(self, app, **kwargs):
        if kwargs.get('elasticsearch_config', None):
            config = kwargs.get('elasticsearch_config')
        else:
            config = get_config(app)['INDEX_SETTINGS']   

        index = get_config(app)['INDEX']

        es = app.extensions['elasticsearch']

        # create or udpate index
        es.indices.create(index=index, ignore=400, body=config)

    def publish_effective_secinfo(self, query, _type, id_field):
        docs = []
        bulk_max = current_app.config['BULK_MAX']
        es = current_app.extensions['elasticsearch']
        es_index = current_app.config['ELASTICSEARCH_INDEX']

        index_name = current_app.config['ELASTICSEARCH_INDEX']

        for item in query:
            docs.append({
                "index": {
                    "_index": es_index,
                    "_type": _type,
                    "_id": item[id_field]
                }
            })
            docs.append({
                'symbol': item['symbol'],
                'floorCode': item['floorcode'],
                'type': item['type'],
                'basic': item['basic'],
                'ceil': item['ceil'],
                'floor': item['floor'],
                'match': item['match'],
                'status': item['status'],
                'currentRoom': item['currentroom'],
                'tradingDate': item['trading_date'] })

            if len(docs) >= bulk_max:
                es.bulk(index=es_index, body=docs)
                docs[:] = []
        if docs:
            es.bulk(index=es_index, body=docs)