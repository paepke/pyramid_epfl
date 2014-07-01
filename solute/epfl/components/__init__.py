# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

from form.form import Form    # A web-form component based on WTForms
from table.table import Table # A data-table component
from menu.menu import Menu # A menu component
from canvas.canvas import Canvas # A canvas component

from containers.boxes import Box




def add_routes(config):
    Form.add_pyramid_routes(config)
    Table.add_pyramid_routes(config)
    Menu.add_pyramid_routes(config)
    Canvas.add_pyramid_routes(config)
    Box.add_pyramid_routes(config)

