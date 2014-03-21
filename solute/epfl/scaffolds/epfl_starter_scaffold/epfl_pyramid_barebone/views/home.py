#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl
import wtforms
import time

DATA = []

for i in range(100):
    DATA.append({
        "icon_edit": {"link": "/redakteure/testberichte_formular/%s" % i},
        "icon_add_product_review": {"link": "/produkttests/produkttests_formular/new_by_report_id/%s" % i},
        "reports.id": i,
        "title": "title %i" % i,
        "review_count": '%s ( %s )' % (i, 100 - i),
        "author": "Gunter"
        })


def get_like_categories_as_domain(prefix, leaves_only=False, try_id_fetch=False):
    """
    returns a list of dicts which starts with the defined prefix
    :return:
    """

    if try_id_fetch:
        try:
            category_id = int(prefix)
            category = Category.by_id(category_id)
            if leaves_only:
                if category['is_leaf']:
                    return [{'label': category['name'], 'value': category['id']}]
            else:
                return [{'label': category['name'], 'value': category['id']}]
        except:
            pass

    category_list = []
    datadict_items = CategoryLikeCollection.beginswith(prefix, is_leaf=leaves_only)
    for id, name in datadict_items.iteritems():
        category_list.append({'label': name,
                              'value': id})
    return category_list

class ReportTable(epfl.components.Table):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    height = 100
    caption = "Meine offenen Testberichte"


    columns_def = [{"name": "icon_edit", "label": "txt_edit", "type": "icon", "sortable": False, "resizable": False,
                                    "default": {"src": "epfl_pyramid_barebone:static/edit_16x16.png", "tip": u"txt_edit_report"},
                                    "width": 20},
                   {"name": "icon_delete", "label": "txt_del", "type": "icon", "sortable": False, "resizable": False,
                                    "default": {"src": "epfl_pyramid_barebone:static/delete_16x16.png", "tip": u"txt_delete_report", "cmd": "Delete"},
                                    "width": 20},
                   {"name": "icon_add_product_review", "label": "txt_PT", "type": "icon", "sortable": False, "resizable": False,
                                    "default": {"src": "epfl_pyramid_barebone:static/add_16x16.png", "tip": u"txt_new_product_review"},
                                    "width": 20},
                   {"name": "reports.status_comment", "label": "txt_S", "type": "icon", "sortable": True, "resizable": False,
                                    "default": {"src": "epfl_pyramid_barebone:static/bearbeitungsvermerk_16x16.png", "tip": u""},
                                    "width": 20},
                   {"name": "reports.id", "label": "txt_id", "type": "id", "sortable": True, "resizable": True, 'default': '', "width": 60},
                   {"name": "title", "label": "txt_headline", "type": "text", "sortable": True, "resizable": True, 'default': ''},
##                   {"name": "date", "label": "txt_date", "type": "text", "sortable": True, "resizable": True, 'default': ''},
                   {"name": "review_count", "label": "txt_product_count", "type": "text", "sortable": True, "resizable": True, 'default': ''},
                   {"name": "author", "label": "txt_author", "type": "text", "sortable": True, "resizable": True, 'default': ''},
##                   {"name": "users.symbol", "label": "txt_redakteuer", "type": "text", "sortable": False, "resizable": True, 'default': ''},
##                   {"name": "reports.editorial_status_id", "label": "txt_status", "type": "text", "sortable": True, "resizable": True, 'default': ''}
                   ]


    def getData(self, start_row, num_rows, sort_column, sort_order):

        data = DATA[:]

        return len(DATA), data[start_row:start_row + num_rows]

    def handle_Delete(self):
        self.show_confirm(u"Testbericht und alle darin enthaltenen Produkttests wirklich löschen?", cmd_ok = "DeleteConfirmed")

    def handle_DeleteConfirmed(self):
        row_id = self.getTargetRowId()
##        report = DB_Report.get_by_id(row_id)
##        product_reviews, count_full = DB_ProductReview.get_by_report_id(row_id)
##        for p in product_reviews:
##            p.delete()
##        report.delete()
        self.refresh_data()



class Menu(epfl.components.Menu):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    menu_def = {'items':[{"label": "Dashboard", "route": "home"},
                         {"label": "Publikationen", "route": "publikationen",
                               "items": [{"label": u"Übersicht", "route": "publikationen"},
                                         {"label": "neue Publikationen", "route": "publikationen_formular"}
                                         ]
                          },

                        ]}



class FilterForm(epfl.components.Form):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    status = epfl.fields.Sort(u"Sortiererei",
                              description = u"Hier kannst mal schön rumsortieren!")

    save = epfl.fields.Button(on_click = "submit")

    test_value1 = epfl.fields.Entry("Click Time", default = "Click-a-me!", description = u"This one will be populated by clicking on 'Click'!")
    test_value2 = epfl.fields.Entry("Text Field (16)", type = "char(16)", validators = [wtforms.validators.Email()])
    test_value3 = epfl.fields.Entry("Integer Field", type = "int", default = 4711)
    test_value5 = epfl.fields.Entry("Mandatory Integer", type = "int", mandatory = True)
    test_value4 = epfl.fields.Entry("Float Field", type = "float")
    test_value6 = epfl.fields.AutoComplete("Autocomplete", type = "int", get_data = "self.get_categories_like")
    test_value7 = epfl.fields.TextArea("Area of Text!")
    test_value8 = epfl.fields.Select("The select", type = "int", choices = "self.get_choices()")

    click = epfl.fields.Button(on_click = "click")
    reset = epfl.fields.Button(on_click = "reset")
    hide = epfl.fields.Button(on_click = "hide")

    toggle_table = epfl.fields.Button(on_click = "ToggleTable")

    def init_transaction(self):

        self.status.data = [(1, "huhu (first)"), (5, "haha (second)"), (10, "hihi (last)")]

        self.set_data({"test_value4": 3.14,
                       "other_value1": time.ctime()})

    def get_choices(self):
        return [(None, "Nix"), (1, "Eins"), (2, "Zwei"), (3, "Drei"), (4, "Fia")]

    def do_post(self):
        if self.validate():
            print "Postie all OK:", self.get_data()
        else:
            print "Postie Errors!"

    def get_categories_like(self, value):
        domain = get_like_categories_as_domain(value, leaves_only=True, try_id_fetch=True)
        return domain


    def handle_click(self):

        self.test_value1.data = "Blubber: " + time.ctime()

        if self.validate():
            print "all OK:", self.get_data()
        else:
            print "Errors!"

        self.redraw()

    def handle_reset(self):
        self.set_visible()
        self.redraw()

    def handle_hide(self):
        self.test_value1.set_hidden()
        self.test_value5.set_hidden()
        self.test_value4.set_hidden()
        self.status.set_hidden()
        self.redraw()

    def handle_ToggleTable(self):
        if self.page.report_table1.is_visible():
            self.page.report_table1.set_hidden()
        else:
            self.page.report_table1.set_visible()

        self.page.report_table1.redraw()


@view_config(route_name = "publikationen")
class PublicationsPage(epfl.Page):

    __acl__ = [(security.Allow, security.Everyone, 'access')]


@view_config(route_name = "publikationen_formular")
class PublicationEditPage(epfl.Page):

    __acl__ = [(security.Allow, security.Everyone, 'access')]


@view_config(route_name='home')
class HomePage(epfl.Page):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template = "home.html"

    def setup_components(self):


        self.menu = Menu()
        self.info_box = epfl.components.Box()
        self.table_box = epfl.components.Box()
        self.report_table1 = ReportTable()
        self.report_table2 = ReportTable()
        self.form = FilterForm()


        self.data["user"] = "DA DUMMY" # self.request.user
