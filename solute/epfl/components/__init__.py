# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

from form.form import Form    # A web-form component based on WTForms
from table.table import Table # A data-table component
from menu.menu import Menu # A menu component
from canvas.canvas import Canvas # A canvas component
from flipflop.flipflop import FlipFlop
from containers.boxes import Box
from sortable.sortable import Sortable
from containers.panel import Panel
from droppable.droppable import Droppable, SimpleDroppable
from dragable.dragable import Dragable
from form_components.form import Button as cfButton
from form_components.form import Input as cfInput
from form_components.form import Form as cfForm
from form_components.form import Text as cfText
from form_components.form import Number as cfNumber
from form_components.form import Checkbox as cfCheckbox
from form_components.form import Textarea as cfTextarea
from form_components.form import Select as cfSelect
from form_components.form import Radio as cfRadio
from form_components.form import Buttonradio as cfButtonradio
from form_components.form import Toggle as cfToggle
from form_components.form import MultiSelect as cfMultiSelect
from badge.badge import Badge
from button.button import Button
from diagram.diagram import Diagram
from progress.progress import Progress
from image.image import Image, ImageList
from layout.col import ColLayout
from layout.cardinal import CardinalLayout
from layout.list import ListLayout
from layout.list import PrettyListLayout
from layout.list import PaginatedListLayout
from layout.nav import NavLayout
from layout.tabs import TabsLayout
from containers.table import TableContainer
from datagrid.datagrid import DataGrid
from simpletable.simpletable import SimpleTable
from datatable.datatable import DataTable
from multiselect.multiselect import MultiSelect, MultiSelectTransfer

def add_routes(config):
    Form.add_pyramid_routes(config)
    Table.add_pyramid_routes(config)
    Menu.add_pyramid_routes(config)
    Canvas.add_pyramid_routes(config)
    Box.add_pyramid_routes(config)
    FlipFlop.add_pyramid_routes(config)
    Sortable.add_pyramid_routes(config)
    Droppable.add_pyramid_routes(config)
    Dragable.add_pyramid_routes(config)
    cfForm.add_pyramid_routes(config)
    Badge.add_pyramid_routes(config)
    Button.add_pyramid_routes(config)
    Diagram.add_pyramid_routes(config)
    Progress.add_pyramid_routes(config)
    Image.add_pyramid_routes(config)
    ColLayout.add_pyramid_routes(config)
    DataGrid.add_pyramid_routes(config)
    SimpleTable.add_pyramid_routes(config)
    DataTable.add_pyramid_routes(config)
    MultiSelect.add_pyramid_routes(config)
    

