#* coding: utf-8

from zope.interface import Interface

class IEpflModelClass(Interface):
    pass


def add_epfl_model(config, model_class):
    if hasattr(model_class, "__setup__"):
        model_class.__setup__(config)
    model_name = model_class.__name__.lower()
    config.registry.registerUtility(model_class, IEpflModelClass, name = model_name)


class LazyModelAccessor(object):
    """ Provided by request.epfl_model
    If an model-class named "BinStore" is registered with config.add_epfl_model(BinStore), you can get
    an instance of it from "request.epfl_model.binstore".
    The BinStore-Class may define an classmethod "__setup__" which will be called with "config" as only parameter.
    the "__init__" of BinStore will be called with the request as only parameter.
    """
    

    def __init__(self, request):
        self.request = request
        self.models = {}

    def __getattr__(self, name):

        model_class = self.request.registry.getUtility(IEpflModelClass, name = name)

        return self.make_model(model_class, name)

    def make_model(self, model_class, name):
        if name in self.models:
            return self.models[name]
        else:
            model = model_class(self.request)
            self.models[name] = model
            return model

