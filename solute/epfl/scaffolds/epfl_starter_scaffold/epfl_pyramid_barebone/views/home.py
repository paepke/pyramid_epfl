#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl

Box = epfl.components.Box
Tab = epfl.components.Tab
List = epfl.components.ListLayout
Nav = epfl.components.NavLayout


class HomeRoot(epfl.components.CardinalLayout):
    node_list = [Tab(slot='center',
                     node_list=[Box(title='Test 1'),
                                Box(title='Test 2'),
                                Box(title='Test 3')]),
                 List(slot='west',
                      node_list=[Box(title='List entry 1'),
                                 Box(title='List entry 2')],
                      links=[('This link points to some_resource', '/some_resource'),
                             ('This link points to another_resource', '/another_resource')]),
                 Box(title='Testbox east',
                     slot='east'),
                 Nav(slot='north',
                     links=[('This link points to some_resource', '/some_resource'),
                            ('This link points to another_resource', '/another_resource')]),
                 Box(title='Testbox south',
                     slot='south')]

@view_config(route_name='home')
class HomePage(epfl.Page):
    template_name = 'base.html'
    root_cls = HomeRoot