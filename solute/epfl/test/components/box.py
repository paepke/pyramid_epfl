import unittest
from pyramid import testing
import solute.epfl as epfl
import pyramid_jinja2

from componentbase import ComponentContainerBaseTest


class BoxTest(ComponentContainerBaseTest):
    component = epfl.components.Box
