#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl


class HomeRoot(epfl.components.CardinalLayout):
    node_list = []


@view_config(route_name='home')
class HomePage(epfl.Page):
    template_name = 'base.html'
    root_cls = HomeRoot