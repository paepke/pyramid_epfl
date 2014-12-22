#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl


class HomeRoot(epfl.components.CardinalLayout):
    node_list = [epfl.components.Box(title='Testbox center',
                                     slot='center'),
                 epfl.components.Box(title='Testbox west',
                                     slot='west'),
                 epfl.components.Box(title='Testbox east',
                                     slot='east'),
                 epfl.components.Box(title='Testbox north',
                                     slot='north'),
                 epfl.components.Box(title='Testbox south',
                                     slot='south')]

@view_config(route_name='home')
class HomePage(epfl.Page):
    template_name = 'base.html'
    root_cls = HomeRoot