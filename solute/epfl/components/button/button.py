from solute.epfl.components.form.form import FormBaseComponent

class Button(FormBaseComponent):
    template_name = "button/button.html"
    js_parts = FormBaseComponent.js_parts + ["button/button.js"]

    label = None
    value = None
    event_name = None
    event_target = None
    is_submit = False

    def __init__(self, label=None, value=None, event_name=None, event_target=None, is_submit=False, **extra_params):
        super(Button, self).__init__()
        if not self.event_name:
            raise Exception('Missing event_name for Button component. %s' % self.cid)
        if not self.event_target:
            self.event_target = self.cid
