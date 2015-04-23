# coding: utf-8
from solute.epfl.components import LinkListLayout
from collections2 import OrderedDict


class GroupedLinkListLayout(LinkListLayout):
    css_name = LinkListLayout.css_name + [('solute.epfl.components:grouped_link_list_layout/static',
                                           'grouped_link_list_layout.css')]

    template_name = "grouped_link_list_layout/grouped_link_list_layout.html"
    data_interface = {'id': None,
                      'text': None,
                      'url': None,
                      'menu_group': None}

    @property
    def groups(self):
        groups = OrderedDict()

        for compo in self.components:
            if getattr(compo, 'menu_group', None):
                groups.setdefault(compo.menu_group, {}).setdefault('components', []).append(compo)
                groups[compo.menu_group]['type'] = 'group'
                groups[compo.menu_group]['name'] = compo.menu_group
            else:
                groups.setdefault(compo.cid, {}).setdefault('components', []).append(compo)
                groups[compo.cid]['type'] = 'entry'

        return groups.values()