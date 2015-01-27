from solute.epfl.components import cfInput as Input

class Toggle(Input):
    """
    A form checkbox styled as toggle.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Toggle(label="Enable/Disable user:", name="user_enable_toggle")])
    
    """
    
    input_type = 'toggle'
    validation_type = 'bool'
    
    
    js_name = Input.js_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.js")]
    css_name = Input.css_name + [("solute.epfl.components:toggle/static", "bootstrap-switch.min.css")]
    
    on_text = "an" #: The text to be displayed if toggle is set to on.
    off_text = "aus" #: The text to be displayed if toggle is set to off.
    default = False #: The default value of the toggle.