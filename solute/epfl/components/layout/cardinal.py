# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class CardinalLayout(epflcomponentbase.ComponentTreeBase):
    template_name = "layout/cardinal.html"
    asset_spec = "solute.epfl.components:layout/static"

    _cardinal_components = None

    css_name = ["bootstrap.min.css"]

    def cardinal_components(self, direction='center'):
        if self._cardinal_components is None:
            self._cardinal_components = {'center': [],
                                         'north': [],
                                         'east': [],
                                         'south': [],
                                         'west': []}
            [self._cardinal_components[compo.slot].append(compo) for compo in self.components]

        return self._cardinal_components[direction]

    def has_cardinal(self, direction):
        return len(self.cardinal_components(direction)) > 0
