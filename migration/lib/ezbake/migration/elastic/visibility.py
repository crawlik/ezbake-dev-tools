from elasticsearch import Elasticsearch

from ezbake.base.thriftapi.ttypes import Visibility
from ezbake.thrift.utils import serialize_to_base64
from ezbake.thrift.utils import deserialize_from_base64

#print serialize_to_base64(Visibility(formalVisibility='U'))
#print deserialize_from_base64(Visibility, 'CwABAAAAAVUA')

class EsMigrator(object):
    def __init__(self, es, es_index):
        self._es = es
        self._es_index = es_index

    def addVisibility(self,
                      body,
                      es_type,
                      scroll_time='1m',
                      visibility=Visibility(formalVisibility='U')):
        
        visibility_field = 'ezbake_visibility'
        visibility = serialize_to_base64(visibility)
    
        res = self._es.search(index=self._es_index,
                              doc_type=es_type,
                              search_type='scan',
                              scroll='1m')

        while True:
            scroll_id = res['_scroll_id']
            print 'using scroll_id %d' % (scroll_id)
            res = self._es.scroll(scroll_id=scroll_id, scroll=scroll_time)
            hits = res['hits']['hits']
            if not res or len(hits) == 0: break
            for hit in hits:
                _id = hit['_id']
                body = {"doc": {visibility_field: visibility}}

                self._es.update(index=self._es_index,
                                doc_type=es_type,
                                id=_id,
                                body=body)
