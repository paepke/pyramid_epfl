from pyramid.view import view_config
from pyramid import security
from functools import wraps
from solute.epfl.components import LinkListLayout

from epflacl import epfl_acl, ACL


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
    acl = []

    config = None
    register = []
    counter = {'id': 0}

    def __init__(self, route_name=None, route_pattern=None, permission=None, route_text=None, rank=0):
        """
        Adds a route, adds the view with the given permissions to that route and creates a link that appears in
        :meth:`get_nav_list`.
        For future expansion the parameters of this method might be extended to allow sub-links and fine tuning of link
        order.
        """
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
        self.counter['id'] += 1
        self.register.append({'id': self.counter['id'],
                              'url': self.route_name,
                              'text': self.route_text})

    @property
    def _config(self):
        if self.config:
            return self.config
        raise Exception('No config found, have you added this module in the config entry epfl.active_modules?')

    @staticmethod
    def configure(config):
        EPFLView.config = config

        active_modules = [m.strip() for m in config.registry.settings.get('epfl.active_modules', '').split(',')
                          if m.strip()]
        for m in active_modules:
            config.maybe_dotted(m)

        EPFLView.config = None

    @staticmethod
    def get_nav_list():
        """
        Return a LinkListLayout Component with links to all registered EPFLViews visible if the current user has the
        correct permissions.
        """
        if EPFLView.acl:
            acl_wrapper = epfl_acl(EPFLView.acl, use_as_global=True)
            acl_wrapper(EPFLViewLinks)
            EPFLView.acl = None
        return EPFLViewLinks(links=EPFLView.register)

    @staticmethod
    def register_acl(*args, **kwargs):
        """
        Register ACLs to be used in the navigation provided by EPFLView and as global ACLs. They will only be registered
        as global ACLs if :meth:`the get_nav_list` is called.
        """
        acl = ACL([])
        epfl_acl(*args, **kwargs)(acl)
        EPFLView.acl.extend(acl.__acl__)


class EPFLViewLinks(LinkListLayout):
    pass
