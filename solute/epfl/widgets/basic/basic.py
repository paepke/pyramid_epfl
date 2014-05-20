# -*- coding: utf-8 -*-

from solute.epfl.core import epflwidgetbase, epflfieldbase
import wtforms
from wtforms.widgets.core import HTMLString


class BasicWidget(epflwidgetbase.WidgetBase):

    asset_spec = "solute.epfl.widgets:basic/static"
    js_name = ["basic.js"]

    def handle_ValueChange(self, value):
        self.field.process_formdata([value])



class ButtonWidget(BasicWidget):

    name = "button"
    param_def = {"on_click": epflwidgetbase.EventType,
                }


    template_name = {"template": "basic/basic.html",
                     "html": "button",
                     "js": "basic_js"}

class RadioButtonWidget(BasicWidget):

    name = "radio"

    param_def = {"on_change": epflwidgetbase.EventType,
                 "choices": epflwidgetbase.DomainType
                }

    template_name = {"template": "basic/basic.html",
                     "html": "radio",
                     "js": "basic_js"}



class EntryWidget(BasicWidget):

    name = "entry"
    param_def = {"on_change": epflwidgetbase.EventType,
                 "on_return": epflwidgetbase.EventType,
                }

    template_name = {"template": "basic/basic.html",
                     "html": "entry",
                     "js": "basic_js"}


    def update_data_source(self, data_source):

        if self.field.max_length:
            data_source.maxlength_attr = self.make_html_attribute("maxlength", self.field.max_length)
        else:
            data_source.maxlength_attr = ""



class TextAreaWidget(BasicWidget):

    name = "textarea"
    param_def = {"on_change": epflwidgetbase.EventType,
                }

    template_name = {"template": "basic/basic.html",
                     "html": "textarea",
                     "js": "basic_js"}


class SelectWidget(BasicWidget):

    name = "select"
    param_def = {"on_change": epflwidgetbase.EventType,
                 "choices": epflwidgetbase.DomainType
                }

    template_name = {"template": "basic/basic.html",
                     "html": "select",
                     "js": "basic_js"}


class ButtonSetWidget(BasicWidget):

    name = "buttonset"
    param_def = {"on_change": epflwidgetbase.EventType,
                 "choices": epflwidgetbase.DomainType
                }

    template_name = {"template": "basic/basic.html",
                     "html": "buttonset",
                     "js": "basic_js"}

    def handle_ValueChange(self, value):
        wid = self.form.get_component_id() + "_" + self.field.name
        value = value.replace(wid + '_', '')
        self.field.process_formdata([value])


class CheckboxWidget(BasicWidget):

    name = "checkbox"
    param_def = {"on_change": epflwidgetbase.EventType,
                }

    template_name = {"template": "basic/basic.html",
                     "html": "checkbox",
                     "js": "basic_js"}





class Button(epflfieldbase.FieldBase):
    widget_class = ButtonWidget

class Entry(epflfieldbase.FieldBase):
    widget_class = EntryWidget

class TextArea(epflfieldbase.FieldBase):
    widget_class = TextAreaWidget

class ButtonSet(epflfieldbase.FieldBase):
    widget_class = ButtonSetWidget

class RadioButton(epflfieldbase.FieldBase):
    widget_class = RadioButtonWidget

    def reload_domain(self):
        """ The Domain (choices) of the button set is evaluated again. """
        self.state["params"]["choices"] = self.widget.eval_param("choices")

class Select(epflfieldbase.FieldBase):
    widget_class = SelectWidget

    def reload_domain(self):
        """ The Domain (choices) of the Select-Box is evaluated again. """
        self.state["params"]["choices"] = self.widget.eval_param("choices")

class Checkbox(epflfieldbase.FieldBase):
    default_field_type = 'bool'
    widget_class = CheckboxWidget

    def init_state(self):
        super(Checkbox, self).init_state()

        if self.data is None:
            self.data = False

