# * encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl

Box = epfl.components.Box
Tab = epfl.components.Tab
List = epfl.components.ListLayout
Nav = epfl.components.NavLayout


class HomeRoot(epfl.components.CardinalLayout):
    constrained = True

    node_list = [List(slot='west',
                      node_list=[Box(title='List entry 1'),
                                 Box(title='List entry 2')],
                      links=[('This link points to foo', '/foo'),
                             ('This link points to another_resource', '/another_resource')]),
                 Box(title='Testbox east',
                     slot='east'),
                 Nav(slot='north',
                     links=[('This link points to some_resource', '/some_resource'),
                            ('This link points to another_resource', '/another_resource')],
                     title='Starter Demo App'),
                 Box(title='Testbox south',
                     slot='south')]

    def init_tree_struct(self):
        # Important since we would not want to change the actual node_list with every new transaction.
        out = self.node_list[:]
        out.append(Tab(slot='center',
                       node_list=[Box(title='Test 1'),
                                  Box(title='Test 2'),
                                  Box(title='Test 3')]), )

        return out


class FooRoot(HomeRoot):
    def init_tree_struct(self):
        # Important since we would not want to change the actual node_list with every new transaction.
        out = self.node_list[:]
        out.append(Tab(slot='center',
                       node_list=[Box(title='Foo 1'),
                                  Box(title='Foo 2'),
                                  Box(title='Foo 3')]), )
        return out


@view_config(route_name='home')
class HomePage(epfl.Page):
    root_cls = HomeRoot


@view_config(route_name='foo')
class FooPage(epfl.Page):
    root_cls = FooRoot