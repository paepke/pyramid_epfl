# coding: utf-8


"""
A Dict-Like Object that represents a epfl-transaction
"""


from pprint import pprint
from redis import StrictRedis
import cPickle as pickle
from copy import deepcopy

import types, copy, string, uuid, time

from solute.epfl import json
from collections import MutableMapping


class Transaction(MutableMapping):
    """ An object that encapsulates the transaction-access.
    The transactions are stored in the session.
    A transaction is always bound to a page-obj.
    """

    _data = None
    _data_original = None

    def __init__(self, request, tid=None):
        """ Give tid = None to create a new one """

        self.request = request
        self.session = request.session
        self.tid = tid
        self.created = False

        if not self.tid:
            self.tid = uuid.uuid4().hex
            self.created = True

    def set_page_obj(self, page_obj):
        self["__page__"] = page_obj.get_name()

    def get_page_name(self):
        return self["__page__"]

    def is_created(self):
        """ Is the transaction created this server-roundtrip? """
        return self.created

    def get_id(self):
        return self.tid

    def __get_child_tids(self):

        child_tids = []

        for key in self.session.keys():
            if key.startswith("TA_") and type(self.session[key]) is dict and self.session[key].has_key("__is_transaction__"):
                ptid = self.session[key].get("__pid__")
                if ptid == self.tid:
                    child_tids.append(key[3:])

        return child_tids

    def get_pid(self):
        return self.get("__pid__", None)

    def set_pid(self, pid):
        self["__pid__"] = pid

    def delete(self):
        """
        Deletes this transaction and all child-transactions.
        """
        child_tids = self.__get_child_tids()

        for tid in child_tids:
            trans = Transaction(self.request, tid)
            trans.delete()

        del self.data

    # MutableMapping requirements:
    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def __delitem__(self, key):
        return self.data.__delitem__(key)

    def __contains__(self, key):
        return self.data.__contains__(key)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    # Internal storage handling
    def store(self):
        if self.is_clean:
            return

        store_type = self.request.registry.settings.get('epfl.transaction.store')
        if store_type == 'redis':
            self.redis.setex('TA_%s' % self.tid, 1800, pickle.dumps(self._data))
        elif store_type == 'memory':
            self.memory['TA_%s' % self.tid] = self._data
        else:
            raise Exception('No valid transaction store found!')

    @property
    def data(self):
        if self._data:
            return self._data

        if not self.tid:
            raise Exception('Transaction store was accessed before transaction id was set.')

        default_data = {"overlays": []}

        store_type = self.request.registry.settings.get('epfl.transaction.store')
        if store_type == 'redis':
            data = self.redis.get('TA_%s' % self.tid)
            if data:
                self._data = pickle.loads(data)
            else:
                self._data = default_data
            self._data_original = deepcopy(self._data)
            if not self.is_clean:
                raise Exception("what the fuck? ")
            return self._data
        elif store_type == 'memory':
            self._data = deepcopy(self.memory.setdefault('TA_%s' % self.tid, default_data))
            if self._data == default_data:
                self.created = True
            self._data_original = deepcopy(self._data)
            return self._data
        else:
            raise Exception('No valid transaction store found!')

    @data.deleter
    def data(self):
        del self._data
        del self._data_original

        store_type = self.request.registry.settings.get('epfl.transaction.store')
        if store_type == 'redis':
            self.redis.delete('TA_%s' % self.tid)
        elif store_type == 'memory':
            del self.memory['TA_%s' % self.tid]
        else:
            raise Exception('No valid transaction store found!')

    @property
    def redis(self):
        if getattr(self.request.registry, 'transaction_redis', None) is None:
            redis_url = self.request.registry.settings.get('epfl.transaction.url')
            if not redis_url:
                raise Exception('Transaction redis url not set!')
            self.request.registry.transaction_redis = StrictRedis.from_url(redis_url)
        return self.request.registry.transaction_redis

    @property
    def memory(self):
        if getattr(self.request.registry, 'transaction_memory', None) is None:
            self.request.registry.transaction_memory = {}
        return self.request.registry.transaction_memory

    @property
    def is_clean(self):
        return self._data == self._data_original


def kill_deleted_transactions(request):

    tids = request.get_epfl_request_aux("deleted_tas", default = [])

    for tid in tids:
        del request.session["TA_" + tid]

