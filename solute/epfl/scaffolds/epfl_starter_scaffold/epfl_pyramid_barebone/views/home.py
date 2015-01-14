# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl


class HomeRoot(epfl.components.CardinalLayout):
    pass

@view_config(route_name='home')
class HomePage(epfl.Page):
    root_node = HomeRoot(constrained=True, node_list=[epfl.components.Box(title="Welcome to EPFL!")])
