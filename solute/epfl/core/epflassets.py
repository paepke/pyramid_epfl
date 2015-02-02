from pyramid.view import view_config
from pyramid import security
from functools import wraps


def get_item_or_attr(obj, key):
    """
    Helper function returning the item key from obj or, failing that the attribute key. If both do not exist an
    Exception is raised by getattr.
    """
    try:
        return obj[key]
    except (KeyError, TypeError):
        return getattr(obj, key)


class ModelBase(object):
    """
    Use this class as a base for your own bound models. For any given method identificator a method of its nam prefiload_
    """

    def __init__(self, request):
        self.request = request

    def get(self, compo, key, row, data_interface):
        args, kwargs = row
        output = []
        for row in getattr(self, 'load_' + key)(compo, *args, **kwargs):
            tmp_data = data_interface.copy()
            for k, v in tmp_data.items():
                if type(v) is str:
                    try:
                        v.format()
                        tmp_data[k] = get_item_or_attr(row, tmp_data[k])
                    except KeyError:
                        if type(row) is dict:
                            tmp_data[k] = v.format(**row)
                        else:
                            tmp_data[k] = v.format(**row.__dict__)
                else:
                    tmp_data[k] = get_item_or_attr(row, k)

            output.append(tmp_data)

        return output


class EPFLView(object):
    config = None
    register = []

    def __init__(self, route_name=None, route_pattern=None, permission=None, route_text=None, rank=0):
        self.route_name = route_name
        self.route_text = route_text or self.route_name
        self.route_pattern = route_pattern
        self.permission = permission
        self.rank = rank

        self._config.add_route(self.route_name, self.route_pattern)

        self.add_link()

    def __call__(self, cb):
        self._config.add_view(cb,
                              route_name=self.route_name,
                              permission=self.permission, )
        return cb

    def add_link(self):
        pass

    @property
    def _config(self):
        if self.config:
            return self.config
        raise Exception('No config found, have you added this module in the config entry epfl.active_modules?')

    @staticmethod
    def configure(config):
        EPFLView.config = config

        active_modules = [m.strip() for m in config.registry.settings.get('epfl.active_modules', '').split(',')]
        for m in active_modules:
            config.maybe_dotted(m)

        EPFLView.config = None
