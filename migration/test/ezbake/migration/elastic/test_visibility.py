from elasticsearch import Elasticsearch
from ezbake.base.thriftapi.ttypes import Visibility
from mock import call,Mock,MagicMock
from unittest import TestCase
from ezbake.thrift.utils import serialize_to_base64

from ezbake.migration.elastic.visibility import EsMigrator

class TestVisibility(TestCase):

    def setUp(self):
        self._es = Elasticsearch()
        self._es_index = 'vistest'
        self._es_type = 'test'
        self._scroll_time = '1m'
        self._migrator = EsMigrator(self._es, self._es_index)
        self._visibility = Visibility(formalVisibility='U')

    def testUpdate00(self): self._assertUpdateBehavior(0, 0)
    def testUpdate11(self): self._assertUpdateBehavior(1, 1)
    def testUpdate15(self): self._assertUpdateBehavior(1, 5)
    def testUpdate55(self): self._assertUpdateBehavior(5, 5)

    def _assertUpdateBehavior(self,
                              numBatches,
                              batchSize,
                              visibility=Visibility(formalVisibility='U')):

        batchSizes = [batchSize] * numBatches + [0]

        self._migrator._es.search = MagicMock(return_value={'_scroll_id': 0})
        self._migrator._es.scroll = Mock(side_effect=TestVisibility.MockScrollSideEffect(batchSizes))
        self._migrator._es.update = Mock()

        ###
        self._migrator.addVisibility({}, self._es_type, scroll_time=self._scroll_time, visibility=self._visibility)
        ###

        self._migrator._es.search.assert_called_with(
              doc_type=self._es_type,
              index=self._es_index,
              scroll=self._scroll_time,
              search_type='scan'
            )
        self.assertEqual(
            [call(scroll=self._scroll_time, scroll_id=i)
             for i in range(numBatches+1)],
            self._migrator._es.scroll.call_args_list
            )
        self.assertEqual(
            [call(
                    body={'doc': {'ezbake_visibility': self._b64vis(visibility)}},
                    doc_type=self._es_type,
                    id=i,
                    index=self._es_index
                    )
             for i in range(batchSize)] * numBatches,
            self._migrator._es.update.call_args_list
            )

    def _b64vis(self, visibility):
        return serialize_to_base64(visibility)

    class MockScrollSideEffect():

        def __init__(self, batchSizes):
            self._batchSizes = batchSizes

        def __call__(self, *args, **kw):
            scroll_id = (kw['scroll_id'] if kw.has_key('scroll_id') else 0)
            batchSizes = self._batchSizes[scroll_id]
            print 'called with %d. batchSizes: %d' % (scroll_id, batchSizes)
            return {
                     '_scroll_id': scroll_id + 1,
                     'hits' : {'hits': [{'_id':x} for x in range(batchSizes)]}
                    }

    class MockUpdateSideEffect():
        def __init__(self): pass
        def __call__(self, *args, **kw): pass

