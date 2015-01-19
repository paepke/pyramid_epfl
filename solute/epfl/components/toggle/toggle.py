from solute.epfl.components import cfInput as Input

class Toggle(Input):
    #asset_spec = "solute.epfl.components:toggle/static" todo: fix this
    
    input_type = 'toggle'
    validation_type = 'bool'
    
    
    js_name = Input.js_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.js")]
    css_name = Input.css_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.css")]
    
    on_text = "an"
    off_text = "aus"
    default = False