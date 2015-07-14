from solute.epfl.core import epflcomponentbase


class Form(epflcomponentbase.ComponentContainerBase):
    template_name = "form/form.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts[:]
    js_parts.append("form/form.js")

    asset_spec = "solute.epfl.components:form/static"
    js_name = ["form.js"]

    compo_state = ["_registered_fields", "is_dirty"]

    fields = []
    _registered_fields = None
    validation_errors = []

    validate_hidden_fields = False
    is_dirty = False

    def __init__(self, page, cid, node_list=None, validate_hidden_fields=False, **extra_params):
        super(Form, self).__init__()

    def handle_submit(self):
        pass

    def handle_set_dirty(self):
        self.is_dirty = True

    def register_field(self, field):
        """
        Make a field known to the parent form. Since any component can reside in a form, the child components
        which register themselves as fields have to provide the methods reset() and validate() (see :class:`.FormInputBase`),
        since these are called for all registered fields by the parent form.
        """
        if self._registered_fields is None:
            self._registered_fields = set()
        self._registered_fields.add(field.cid)

    def unregister_field(self,field):
        try:
            self._registered_fields.remove(field.cid)
        except (AttributeError, KeyError):
            pass


    @property
    def registered_fields(self):
        if self._registered_fields is None:
            self._registered_fields = set()
        return [self.page.components[cid] for cid in self._registered_fields]

    @property
    def registered_names(self):
        if self._registered_fields is None:
            self._registered_fields = set()
        return dict([[self.page.components[cid].name, self.page.components[cid]]
                     for cid in self._registered_fields
                     if hasattr(self.page.components[cid], 'name') and self.page.components[cid].name is not None])

    def get_values(self):
        values = {}

        for field in self.registered_fields:
            if field.name is None:
                continue
            values[field.name] = field.converted_value
        return values

    def set_value(self, key, value):
        for field in self.registered_fields:
            if field.name == key:
                field.value = value
                return

    def reset(self):
        """
        Initialize all registered form fields with its default value and clear all validation messages.
        """
        for field in self.registered_fields:
            field.reset()
        self.redraw()

    def validate(self):
        result = []
        for field in self.registered_fields[:]:
            # Do not validate fields without a name, cause they can not contain
            # a value.
            if field.name is None:
                continue
            if not self.validate_hidden_fields and not field.is_visible():
                continue
            validation_result = field.validate()
            result.append(validation_result)

        if False in result:
            self.validation_errors = result
        return not False in result

    def get_errors(self):
        return self.validation_errors
