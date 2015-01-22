from solute.epfl.core import epflcomponentbase

class Sidebar(epflcomponentbase.ComponentContainerBase):
    theme_path = ['sidebar/theme']
    default_child_cls = epflcomponentbase.ComponentContainerBase

    data_interface = {'id': None,
                      'url': None,
                      'name': None,
                      'icon': None,
                      'children':None}


