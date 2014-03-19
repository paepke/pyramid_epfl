# coding: utf-8


"""
A Dict-Like Object that represents a epfl-transaction
"""


from pprint import pprint

import types, copy, string, uuid, time

from solute.epfl import json


class Transaction(object):

    def __init__(self, request):

        self.request = request
        self.session = self.request.session
        self.tid = self.request.get_transaction_id()

        if not self.tid:
            self.tid = str(uuid.uuid4())
            self.request.set_transaction_id(self.tid)
            self.created = True
        else:
            self.created = False

        self.data = self.session.get("TA_" + self.tid)

        if self.created:
            self["__ct__"] = time.time()

    def is_created(self):
        """ Is the transaction created this server-roundtrip? """
        return self.created

    def setup_data(self):
        if self.data is None:
            self.data = self.session["TA_" + self.tid] = {}

    def get_id(self):
        return self.tid

    def set_ptid(self, parent_tid):
        self["__ptid__"] = parent_tid

    def get_ptid(self):
        return self["__ptid__"]

    def __getitem__(self, key):
        if self.data is None:
            return None
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        self.setup_data()
        self.data[key] = value

    def __contains__(self, key):
        return self.has_key(key)

    def get(self, key, default = None):
        if self.has_key(key):
            return self[key]
        else:
            return default

    def has_key(self, key):
        if self.data is None:
            return False
        return self.data.has_key(key)

    def update(self, dict):
        self.setup_data()
        self.data.update(dict)
