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
from droppable.droppable import Droppable
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
from form_components.form import Buttonset as cfButtonset
from form_components.form import Toggle as cfToggle
from badge.badge import Badge
from button.button import Button
from diagram.diagram import Diagram
from progress.progress import Progress
from image.image import Image



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
    #Panel.add_pyramid_routes(config)
    Badge.add_pyramid_routes(config)
    Button.add_pyramid_routes(config)
    Diagram.add_pyramid_routes(config)
    Progress.add_pyramid_routes(config)
    Image.add_pyramid_routes(config)
    

