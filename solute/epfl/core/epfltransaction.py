# coding: utf-8


"""
A Dict-Like Object that represents a epfl-transaction
"""


from pprint import pprint

import types, copy, string, uuid, time

from solute.epfl import json


class Transaction(object):
    """ An object that encapsulates the transaction-access.
    The transactions are stored in the session.
    A transaction is always bound to a page-obj.
    """

    def __init__(self, global_request, tid = None):
        """ Give tid = None to create a new one """

        self.global_request = global_request
        self.session = global_request.session
        self.tid = tid

        if not self.tid:
            self.tid = str(uuid.uuid4())
            self.session["TA_" + self.tid] = {}
            self.created = True
        else:
            self.created = False

        self.data = self.session["TA_" + self.tid]
        self.pid = self.data.get("__pid__")


        if self.created:
            # setup new transaction
            self["is_transaction"] = True
            self["__ct__"] = time.time()
            self["overlays"] = []

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
            if key.startswith("TA_") and type(self.session[key]) is dict and self.session[key].has_key("is_transaction"):
                ptid = self.session[key].get("__pid__")
                if ptid == self.tid:
                    child_tids.append(key[3:])

        return child_tids


    def get_pid(self):
        return self.pid

    def set_pid(self, pid):
        self.pid = pid
        self["__pid__"] = pid

    def __getitem__(self, key):
        if self.data is None:
            return None
        else:
            return self.data[key]

    def __setitem__(self, key, value):
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
        self.data.update(dict)

    def delete(self):
        """
        Marks this transaction for deletion and all child-transactions.
        """

        tids = self.global_request.get_epfl_request_aux("deleted_tas", default = [])
        if self.tid not in tids:
            tids.append(self.tid)
        self.global_request.set_epfl_request_aux("deleted_tas", tids)

        child_tids = self.__get_child_tids()

        for tid in child_tids:
            trans = Transaction(self.global_request, tid)
            trans.delete()


def kill_deleted_transactions(global_request):

    tids = global_request.get_epfl_request_aux("deleted_tas", default = [])

    for tid in tids:
        del global_request.session["TA_" + tid]

