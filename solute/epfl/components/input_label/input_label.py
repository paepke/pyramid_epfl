from solute.epfl.core import epflcomponentbase
from collections2 import OrderedDict as odict


class InputLabel(epflcomponentbase.ComponentBase):

    """
    Renders a single label as used for form input fields, but without
    any input field attached. This component can be used to insert a label
    in a form that renders like the labels for the input fields, but for
    which no form input component is available.
    
    Typically, this component is placed in a ColLayout to adjust it in the same col as other
    input labels.
    
    """
    
    template_name = "input_label/input_label.html"

    compo_state = ['label']  # : The value of the label.
