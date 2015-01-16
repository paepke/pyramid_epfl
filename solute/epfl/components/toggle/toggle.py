from solute.epfl.components import cfInput as Input

class Toggle(Input):
    #asset_spec = "solute.epfl.components:toggle/static" todo: fix this
    
    input_type = 'toggle'
    validation_type = 'bool'
    css_name = Input.css_name[:]
    css_name.append("bootstrap-switch.min.css")
    js_name = Input.js_name[:]
    js_name.append("bootstrap-switch.min.js")
    on_text = "an"
    off_text = "aus"
    default = False