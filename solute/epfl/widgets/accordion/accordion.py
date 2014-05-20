# -*- coding: utf-8 -*-

from solute.epfl.core import epflfieldbase
from solute.epfl.core import epflwidgetbase


class AccordionWidget(epflwidgetbase.WidgetBase):
    """ Displays an accordion which allows
    """

    name = "accordion"
    template_name = "accordion/accordion.html"
    asset_spec = "solute.epfl.widgets:accordion/static"

    js_name = ["accordion.js"]


    param_def = {"sections": epflwidgetbase.DomainType,
                 "on_section_click": epflwidgetbase.EventType,
                 "on_content_click": epflwidgetbase.EventType}

    def handle_ValueChange(self, value):
        wid = self.form.get_component_id() + "_" + self.field.name
        value = value.replace(wid + '_', '')
        self.field.process_formdata([value])

    def handle_SectionClick(self, widget_name = None, **params):
        cmd = self.params["on_section_click"]
        self.form.handle_event(cmd, event_params = params)

    def handle_ContentClick(self, widget_name = None, **params):
        wid = self.form.get_component_id() + "_" + self.field.name
        id_list = params['full_content_id'].replace(wid + '_', '').split('_')
        params['section_id'] = id_list[0]
        params['content_id'] = id_list[1]
        params.pop('full_content_id', None)

        cmd = self.params["on_content_click"]
        self.form.handle_event(cmd, event_params = params)

    def update_data_source(self, data_source):
        data_source.params['sections'] = self.eval_param('sections')


class Accordion(epflfieldbase.FieldBase):
    widget_class = AccordionWidget