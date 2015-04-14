# coding: utf-8


"""
A Dict-Like Object that represents a epfl-transaction
"""

from pprint import pprint
from redis import StrictRedis
import cPickle as pickle
from copy import deepcopy
from collections2 import OrderedDict as odict

import types, copy, string, uuid, time

from collections import MutableMapping, defaultdict
from solute.epfl.core import epflcomponentbase

class Transaction(MutableMapping):
    """ An object that encapsulates the transaction-access.
    The transactions are stored in the session.
    A transaction is always bound to a page-obj.
    """

    #: Internal cache of the data this transaction holds.
    _data = None
    #: Internal cache of the data this transaction held when loaded.
    _data_original = None

    #: Can contain a new transaction id to be used for storing this transaction. If given, the original transaction will
    #: be stored as locked under its original id so that it will be preserved in the state it was left in. Should be
    #: accessed via :meth:`store_as_new`.
    tid_new = None

    #: The transaction id.
    tid = None

    #: True if the Transaction was just created.
    created = False

    #: The request currently in progress.
    request = None
    #: The session of the request currently in progress.
    session = None

    def __init__(self, request, tid=None):
        """ Give tid = None to create a new one """

        self.instances = {}
        self.request = request
        self.session = request.session
        self.tid = tid
        self.created = False

        self.compo_reference = {}

        if not self.tid:
            self.tid = uuid.uuid4().hex
            self.created = True

    def set_page_obj(self, page_obj):
        self["__page__"] = page_obj.get_name()
        self["__initialized_components__"] = set()

    def get_page_name(self):
        return self["__page__"]

    def is_created(self):
        """
        Returns true if the transaction was created this server-roundtrip.
        """
        return self.created

    def get_id(self):
        return self.tid

    def get_pid(self):
        return self.get("__pid__", None)

    def set_pid(self, pid):
        self["__pid__"] = pid

    def delete(self):
        """
        Deletes this transaction and all child-transactions.
        """
        del self.data

    # EPFL Core Api methods
    def get_component_depth(self, cid):
        try:
            return self.get_component_depth(self['compo_lookup'][cid]) + 1
        except KeyError:
            return 0

    def get_existing_components(self):
        return self['compo_lookup'].keys() + self['compo_struct'].keys()

    def get_component_instance(self, page, cid):
        if cid not in self.instances:
            compo_info = self.get_component(cid)
            ubc = epflcomponentbase.UnboundComponent.create_from_state(compo_info['class'])
            self.instances[cid] = ubc(page,
                                      cid,
                                      __instantiate__=True,
                                      **compo_info['config'])
        return self.instances[cid]

    def get_active_components(self):
        return self.instances.values()

    def is_active_component(self, cid):
        return cid in self.instances

    def switch_component(self, cid, ccid, position=None):
        compo_info = self.pop_component(cid)
        compo_info['ccid'] = ccid
        self.set_component(cid, compo_info, position=position)

    def pop_component(self, cid):
        try:
            return self['compo_struct'].pop(cid)
        except KeyError:
            pass

        try:
            return self.pop_child_component(self['compo_lookup'][cid],
                                            cid)
        except KeyError:
            return None

    def get_component(self, cid):
        try:
            return self['compo_struct'][cid]
        except KeyError:
            pass

        try:
            return self.get_child_component(self['compo_lookup'][cid],
                                            cid)
        except KeyError:
            return None

    def get_child_component(self, ccid, cid):
        compo = self.get_component(ccid)
        try:
            return compo['compo_struct'][cid]
        except (TypeError, KeyError):
            return None

    def pop_child_component(self, ccid, cid):
        compo = self.get_component(ccid)
        try:
            return compo['compo_struct'].pop(cid)
        except (TypeError, KeyError):
            return None

    def set_component(self, cid, compo_info, position=None, compo_obj=None):
        if not isinstance(compo_info, dict):
            compo_obj = compo_info
            compo_info = compo_obj.get_component_info()
        if compo_obj:
            self.instances[cid] = compo_obj

        container = self
        if 'ccid' in compo_info:
            self.setdefault('compo_lookup', {})[cid] = compo_info['ccid']
            container = self.get_component(compo_info['ccid'])
        if 'cid' not in compo_info:
            compo_info['cid'] = cid

        compo_struct = container.setdefault('compo_struct', odict())
        if position is None:
            compo_struct[cid] = compo_info
        else:
            compo_struct.insert(cid, compo_info, position)

    def del_component(self, cid):
        compo = self.get_component(cid)
        container = self
        if 'ccid' in compo:
            container = self.get_component(compo['ccid'])

        for child_cid in compo.get('compo_struct', {}).keys():
            if self.has_component(child_cid):
                self.del_component(child_cid)

        if 'compo_lookup' in self and cid in self['compo_lookup']:
            del self['compo_lookup'][cid]
        if cid in self.instances:
            del self.instances[cid]
        if cid in container['compo_struct']:
            del container['compo_struct'][cid]

    def has_component(self, cid):
        try:
            return self.get_component(cid) is not None
        except KeyError:
            return False

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
    def lock_transaction(self):
        """
        Load a copy of the current transaction, unset the flag requesting a new transaction, reset the lock status and
        store it as locked. After calling this the transaction related to this :class:`Transaction` instance should be
        stored under a new transaction id, else it would override the locked copy.
        """
        old_transaction = Transaction(self.request, self.tid)
        old_transaction.tid_new = None
        old_transaction.pop('locked', None)
        old_transaction.store(lock=True)

    def store_as_new(self):
        """
        Generate a fresh transaction id using the uuid module.
        """
        self.tid_new = uuid.uuid4().hex

    def store(self, lock=False):
        """
        Recursive storing mechanism. If no changes have occurred during this request nothing is done. If the transaction
        is locked because it has spawned a child transaction a new transaction will be generated. If a new transaction
        has been requested the current transaction is stored locked and a new unlocked transaction with the same content
        is stored in its stead.
        """
        if self.is_clean and not lock:
            return

        if self.pop('locked', False):
            self.store_as_new()

        if lock:
            self['locked'] = lock

        if self.tid_new:
            self.lock_transaction()
            self.tid = self.tid_new

        store_type = self.request.registry.settings.get('epfl.transaction.store')
        transaction_timeout = self.request.registry.settings.get('epfl.transaction.timeout', 1800)
        if store_type == 'redis':
            self.redis.setex('TA_%s' % self.tid, transaction_timeout, pickle.dumps(self._data))
        elif store_type == 'memory':
            self.memory['TA_%s' % self.tid] = self._data
        else:
            raise Exception('No valid transaction store found!')

    @property
    def data(self):
        """
        Get data from the configured storage system.
        """
        if self._data:
            return self._data

        if not self.tid:
            raise Exception('Transaction store was accessed before transaction id was set.')

        default_data = {}

        store_type = self.request.registry.settings.get('epfl.transaction.store')
        if store_type == 'redis':
            data = self.redis.get('TA_%s' % self.tid)
            if data:
                self._data = pickle.loads(data)
                self._data_original = pickle.loads(data)
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
        """
        Delete the transaction from its respective Storage.
        """
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
        """
        Redis storage abstraction layer. Returns a singleton with get, delete and set methods.
        """
        if getattr(self.request.registry, 'transaction_redis', None) is None:
            redis_url = self.request.registry.settings.get('epfl.transaction.url')
            if not redis_url:
                raise Exception('Transaction redis url not set!')
            self.request.registry.transaction_redis = StrictRedis.from_url(redis_url)
        return self.request.registry.transaction_redis

    @property
    def memory(self):
        """
        Memory storage abstraction layer. Returns a singleton dictionary.
        """
        if getattr(self.request.registry, 'transaction_memory', None) is None:
            self.request.registry.transaction_memory = {}
        return self.request.registry.transaction_memory

    @property
    def is_clean(self):
        """
        Returns true if the transaction has not been changed.
        """
        return self._data == self._data_original

