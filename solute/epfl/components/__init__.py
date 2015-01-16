# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

from menu.menu import Menu # A menu component
from canvas.canvas import Canvas # A canvas component
from flipflop.flipflop import FlipFlop
from box.box import Box
from sortable.sortable import Sortable
from panel.panel import Panel
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
from tabs_layout.tabs_layout import TabsLayout
from nav_layout.nav_layout import NavLayout
from col_layout.col_layout import ColLayout
from cardinal_layout.cardinal_layout import CardinalLayout
from list_layout.list_layout import ListLayout
from pretty_list_layout.pretty_list_layout import PrettyListLayout
from toggle_list_layout.toggle_list_layout import ToggleListLayout
from paginated_list_layout.paginated_list_layout import PaginatedListLayout
from link_list_layout.link_list_layout import LinkListLayout
from hover_link_list_layout.hover_link_list_layout import HoverLinkListLayout
from table_list_layout.table_list_layout import TableListLayout

from containers.table import TextValue
from simpletable.simpletable import SimpleTable
from multiselect.multiselect import MultiSelect, MultiSelectTransfer


def add_routes(config):
    """
    Called once per thread start, in order to call
    :func:`solute.epfl.core.epflcomponentbase.ComponentBase.add_pyramid_routes` for every component provided by epfl
    through this package.
    """
    
    
    Canvas.add_pyramid_routes(config)
    Box.add_pyramid_routes(config)
    TabsLayout.add_pyramid_routes(config)
    NavLayout.add_pyramid_routes(config)
    ColLayout.add_pyramid_routes(config)
    CardinalLayout.add_pyramid_routes(config)
    Panel.add_pyramid_routes(config)
    
    ListLayout.add_pyramid_routes(config)
    PrettyListLayout.add_pyramid_routes(config)
    ToggleListLayout.add_pyramid_routes(config)
    PaginatedListLayout.add_pyramid_routes(config)
    LinkListLayout.add_pyramid_routes(config)
    HoverLinkListLayout.add_pyramid_routes(config)
    TableListLayout.add_pyramid_routes(config)
    
    
    SimpleTable.add_pyramid_routes(config)
    MultiSelect.add_pyramid_routes(config)
    Menu.add_pyramid_routes(config)
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
    
    TextValue.add_pyramid_routes(config)

