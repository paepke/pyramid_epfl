#* coding: utf-8

from zope.interface import Interface, implements


# the interfaces:

class ITempDataProvider(Interface):
    """ A TempDataProvider must be able to store large binary data at least
    the life-time of a session. 
    It is only responsible for storing the data. The GC must be implemented
    at a higher level.
    """

    def __init__(self, config):
        pass
    
    def get(self, request, key, default = None):
        pass

    def set(self, request, key, value):
        pass

    def delete(self, request, key):
        pass


class INodeGlobalDataProvider(Interface):
    """ A GlobalDataProvider must be able to store not so large python objects
    for at least the life-time of the server process.
    No GC neccesary.
    """

    def __init__(self, config):
        pass



class LocalMemoryProvider(object):
    """ Does what it is called.
    Not suitable for production as TempDataProvider, because it uses up the main-memory and
    can not be used in a clustered system.
    As GlobalDataProvider you can use it in production.
    """

    def __init__(self, config):
        self.blobs = {}

    def get(self, request, key, default = None):
        return self.blobs.get(key, default)

    def set(self, request, key, value):
        self.blobs[key] = value


# the request-methods:

def get_epfl_temp_blob(request, key):
    """ Store/Retrieve a possibliy very large binary object temporarily but avaiable on all nodes. """
    provider = request.registry.queryUtility(ITempDataProvider)
    if not provider:
        raise ValueError, "No ITempDataProvider configured!"
    return provider.get(request, key)

def set_epfl_temp_blob(request, key, value):
    """ Store/Retrieve a possibliy very large binary object temporarily but avaiable on all nodes. """
    provider = request.registry.queryUtility(ITempDataProvider)
    if not provider:
        raise ValueError, "No ITempDataProvider configured!"
    provider.set(request, key, value)

def get_epfl_nodeglobal_aux(request, key, default = None):
    provider = request.registry.queryUtility(INodeGlobalDataProvider)
    if not provider:
        raise ValueError, "No IGlobalDataProvider configured!"
    return provider.get(request, key, default)

def set_epfl_nodeglobal_aux(request, key, value):
    provider = request.registry.queryUtility(INodeGlobalDataProvider)
    if not provider:
        raise ValueError, "No IGlobalDataProvider configured!"
    provider.set(request, key, value)

