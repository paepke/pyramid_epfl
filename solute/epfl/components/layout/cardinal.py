# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class CardinalLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "layout/cardinal.html"
    asset_spec = "solute.epfl.components:layout/static"

    _cardinal_components = None

    css_name = ["bootstrap.min.css"]

    compo_state = ['constrained']

    constrained = False

    def cardinal_components(self, direction='center'):
        if self._cardinal_components is None:
            self._cardinal_components = {'center': [],
                                         'north': [],
                                         'east': [],
                                         'south': [],
                                         'west': []}
            for compo in self.components:
                self._cardinal_components.setdefault(getattr(compo, 'slot', None) or 'center', []).append(compo)

        return self._cardinal_components.get(direction, [])

    def has_cardinal(self, direction):
        return len(self.cardinal_components(direction)) > 0
