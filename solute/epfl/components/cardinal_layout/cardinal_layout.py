# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class CardinalLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "cardinal_layout/cardinal_layout.html"
    asset_spec = "solute.epfl.components:cardinal_layout/static"

    _cardinal_components = None


    compo_state = ['constrained']

    constrained = None

    def cardinal_components(self, direction='center'):
        if self._cardinal_components is None:
            self._cardinal_components = {'center': [],
                                         'north': [],
                                         'east': [],
                                         'south': [],
                                         'west': []}
            for compo in self.components:
                self._cardinal_components.setdefault(getattr(compo, 'container_slot', None) or 'center', []).append(compo)

        return self._cardinal_components.get(direction, [])

    def has_cardinal(self, direction):
        return len(self.cardinal_components(direction)) > 0
