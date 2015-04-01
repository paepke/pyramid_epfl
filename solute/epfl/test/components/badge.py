import unittest
from pyramid import testing
import solute.epfl as epfl
import pyramid_jinja2

from componentbase import ComponentBaseTest


class BadgeTest(ComponentBaseTest):
    component = epfl.components.Badge
