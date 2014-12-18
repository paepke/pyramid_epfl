from solute.epfl.core import epflcomponentbase
from solute.epfl.components.form_components.form import Input

def Toggle(label=None, name=None, default=False, validation_helper=None, **extra_params):
    myToggle =  epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='checkbox',
                                                                validation_type='bool',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                asset_spec = "solute.epfl.components:toggle/static",
                                                                js_name = ["bootstrap-switch.min.js"],
                                                                css_name = ["bootstrap-switch.min.css"],
                                                                **extra_params)],
                                               template_name='toggle/toggle.html',
                                               label=label)
    return myToggle