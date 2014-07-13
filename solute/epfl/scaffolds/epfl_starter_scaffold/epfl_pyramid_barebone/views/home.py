#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl
import time, datetime


@view_config(route_name='home')
class HomePage(epfl.Page):

    template = "home.html"

    def setup_components(self):
        pass

