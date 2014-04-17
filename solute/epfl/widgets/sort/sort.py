# -*- coding: utf-8 -*-

from solute.epfl.core import epflwidgetbase, epflfieldbase


class SortWidget(epflwidgetbase.WidgetBase):
    """ Displays a select-box with the posibility to sort the displayed items.
    To be used with a "SelectMultipleField" !
    """

    name = "sort"
    template_name = "sort/sort.html"
    asset_spec = "solute.epfl.widgets:sort/static"

    js_name = ["sort.js"]
    css_name = ["sort.css"]
    param_def = {"on_change": (epflwidgetbase.EventType, None),
                 "on_click": (epflwidgetbase.EventType, None),
                 }


    def setup_state(self):
        super(SortWidget, self).setup_state()

        idx_list = [int(idx) for idx in self.request.getall("_idx_" + self.field.name)]

        if idx_list:
            # update by query-params
            self.field.data = []
            value = self.state["value"]
            for idx in idx_list:
                self.field.data.append(value[idx])
        else:
            # restore from state
            if "value" in self.state:
                self.field.data = self.state["value"]


    def finalize_state(self):
        self.state["value"] = self.field.data

    def update_data_source(self, data_source):
        style = data_source.kwargs.get('style', '')
        data_source.style = style

        class_ = data_source.kwargs.get('class_', '')
        data_source.class_ = class_

        idx = 0
        all_items = []
        for value, label in data_source.value or []:
            all_items.append({"idx": idx,
                              "label": label})
            idx += 1
        data_source.all_items = all_items


    def handle_ValueChange(self, idx_list):

        self.field.data = []
        value = self.state["value"]
        for idx in idx_list:
            self.field.data.append(value[idx])

        js = self.js_call("this.reset_idx")
        self.form.add_js_response(js)



class Sort(epflfieldbase.FieldBase): 
    widget_class = SortWidget
