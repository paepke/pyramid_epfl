# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

from form.form import Form    # A web-form component based on WTForms
from table.table import Table # A data-table component
from menu.menu import Menu # A menu component
from canvas.canvas import Canvas # A canvas component

from containers.boxes import Box




def add_static_routes(config):
    config.add_static_view(name = "epfl/components/form", path = "solute.epfl.components:form/static")
    config.add_static_view(name = "epfl/components/containers", path = "solute.epfl.components:containers/static")
    config.add_static_view(name = "epfl/components/menu", path = "solute.epfl.components:menu/static")
    config.add_static_view(name = "epfl/components/table", path = "solute.epfl.components:table/static")

