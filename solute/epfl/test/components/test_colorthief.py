# * encoding: utf-8

from __future__ import unicode_literals
from lxml import etree

from solute.epfl import components


def test_render_with_no_options(page):
    page.root_node = components.ColorThief(
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())
    assert compo_html.attrib.get('epflid', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('id', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('class', None) == "epfl-colorthief", "epflid not found"

    dropzone = compo_html.find("div[@class='epfl-colorthief-dropzone text-center']")
    assert dropzone is not None, "No Dropzone found"
    assert dropzone.find("i") is not None, "No icon in Dropzone found"

    img = compo_html.find("img[@class='epfl-colorthief-image']")
    assert img is not None, "Could not found image"
    assert img.attrib.get("data-cid", None) == "%s" % compo.cid, "image has no or wrong data-cid attribute"


def test_render_with_options(page):
    page.root_node = components.ColorThief(
        height=250,
        width=150,
        image_src="test.png"
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())
    assert compo_html.attrib.get("style", None) == "height:250px; width:150px;", "Height and Width not set"
    remove_icon = compo_html.find("i[@class='fa fa-times fa-lg color-danger epfl-colorthief-remove-icon']")
    assert remove_icon is not None, "No remove icon found"

    img = compo_html.find("img[@class='epfl-colorthief-image']")
    assert img is not None, "Could not found image"
    assert img.attrib.get("src", None) == "test.png", "Image src not set"


def test_change(page):
    page.root_node = components.ColorThief(
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() is None, "Wrong default value"
    assert compo.image_src is None, "Wrong default image_src"

    compo.handle_change(value=[(255, 255, 255), (0, 0, 0)], image_src="test.png")

    compo.render_cache = None
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() == [{u'rgb': u'#ffffff', u'selected': False},
                                 {u'rgb': u'#000', u'selected': False}], "Wrong value after handle change"
    assert compo.image_src == "test.png", "wrong image_src after handle_change"

    color_divs = compo_html.findall("div[@class='epfl-colorthief-color pull-left text-center']")
    assert len(color_divs) == 2, "No or not all color divs got renderd"
    assert color_divs[0].attrib.get("style", None) == "background-color: #ffffff", "white color div has no color"
    assert color_divs[1].attrib.get("style", None) == "background-color: #000", "black color div has no color"
    assert color_divs[0].attrib.get("data-color", None) == "#ffffff", "white color div has no data-color"
    assert color_divs[1].attrib.get("data-color", None) == "#000", "black color div has no data-color"

    compo.handle_click_color("#000")
    compo.render_cache = None
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() == [{u'rgb': u'#ffffff', u'selected': False},
                                 {u'rgb': u'#000', u'selected': True}], "Wrong value after handle_click_color"

    color_divs = compo_html.findall("div[@class='epfl-colorthief-color pull-left text-center']")
    assert len(color_divs[1]) == 1, "Selected color div has no icon"

    compo.handle_click_color("#000")
    compo.render_cache = None
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() == [{u'rgb': u'#ffffff', u'selected': False},
                                 {u'rgb': u'#000', u'selected': False}], "Wrong value after handle_click_color"

    color_divs = compo_html.findall("div[@class='epfl-colorthief-color pull-left text-center']")
    assert len(color_divs[1]) == 0, "Selected color div has a icon after deselect"
