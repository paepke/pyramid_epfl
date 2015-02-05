# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

from canvas.canvas import Canvas  # A canvas component
from flipflop.flipflop import FlipFlop
from box.box import Box
from drag_box.drag_box import DragBox
from droppable_box.droppable_box import DroppableBox
from sortable.sortable import Sortable
from panel.panel import Panel
from droppable.droppable import Droppable, SimpleDroppable
from dragable.dragable import Dragable

from form.form import Form
from button.button import Button
from text_input.text_input import TextInput
from number_input.number_input import NumberInput
from checkbox.checkbox import Checkbox
from textarea.textarea import Textarea
from select.select import Select
from radio.radio import Radio
from buttonradio.buttonradio import ButtonRadio
from toggle.toggle import Toggle
from password_input.password_input import PasswordInput

from sidebar.sidebar import Sidebar
from headbar.headbar import Headbar

from badge.badge import Badge
from diagram.diagram import Diagram
from progress.progress import Progress
from image.image import Image, ImageList
from text.text import Text
from placeholder.placeholder import Placeholder

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
from tree_layout.tree_layout import TreeLayout, TreeLeafEntry, DraggableTreeLeafEntry, DroppableTreeLayout

from simpletable.simpletable import SimpleTable
from multiselect.multiselect import MultiSelect, MultiSelectTransfer

from modal.modal import Modal


def add_routes(config):
    """
    Called once per thread start, in order to call
    :func:`solute.epfl.core.epflcomponentbase.ComponentBase.add_pyramid_routes` for every component provided by epfl
    through this package.
    """

    Canvas.add_pyramid_routes(config)
    Box.add_pyramid_routes(config)
    DragBox.add_pyramid_routes(config)
    DroppableBox.add_pyramid_routes(config)
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
    TreeLayout.add_pyramid_routes(config)

    SimpleTable.add_pyramid_routes(config)
    MultiSelect.add_pyramid_routes(config)
    FlipFlop.add_pyramid_routes(config)
    Sortable.add_pyramid_routes(config)
    Droppable.add_pyramid_routes(config)
    Dragable.add_pyramid_routes(config)

    Form.add_pyramid_routes(config)
    Button.add_pyramid_routes(config)
    TextInput.add_pyramid_routes(config)
    NumberInput.add_pyramid_routes(config)
    Textarea.add_pyramid_routes(config)
    Radio.add_pyramid_routes(config)
    ButtonRadio.add_pyramid_routes(config)
    Toggle.add_pyramid_routes(config)
    Checkbox.add_pyramid_routes(config)
    Select.add_pyramid_routes(config)

    Badge.add_pyramid_routes(config)
    Diagram.add_pyramid_routes(config)
    Progress.add_pyramid_routes(config)
    Image.add_pyramid_routes(config)
    Text.add_pyramid_routes(config)
    Sidebar.add_pyramid_routes(config)
    Headbar.add_pyramid_routes(config)
    Placeholder.add_pyramid_routes(config)

    Modal.add_pyramid_routes(config)
