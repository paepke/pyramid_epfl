from solute.epfl.core.epflcomponentbase import ComponentBase

class Button(ComponentBase):
    """
    This component provides basic button functionality.
    
    To use a button, a event handling method for handling button clicks has to be provided:
    
    .. code:: python
        
        button = Button(name="Do something", event_name="submit")
        
        def handle_submit(self):
            pass
            # do something: button has been clicked

    """

    asset_spec = "solute.epfl.components:button/static"
    template_name = "button/button.html"
    js_parts = ["button/button.js"]
    js_name = ["button.js"]
    compo_state = ComponentBase.compo_state + ['disabled']

    label = None #: If set, the label is rendered before the button.
    value = None #: The value is used as button text if no icon is provided.
    icon = None #: Optional font-awesome icon to be rendered as button value instead of :attr:`value` text.
    event_name = None #: Mandatory name of the event handling method (without trailing "handle\_").
    event_target = None #: Optional target where the event handling method can be found.
    is_submit = False #: Set to true if button should have html type "submit".
    disabled = False #: Set to true if button should be disabled.
    confirm_first = False #: Set to true if user should be asked for confirmation first before the button event is triggered
    confirm_message = "Do you want to proceed?" #: Adapt this text for a custom confirmation dialog message.

    def __init__(self, label=None, value=None, event_name=None, event_target=None, is_submit=False, **extra_params):
        super(Button, self).__init__()
        if not self.event_name:
            raise Exception('Missing event_name for Button component. %s' % self.cid)
        if not self.event_target:
            self.event_target = self.cid
