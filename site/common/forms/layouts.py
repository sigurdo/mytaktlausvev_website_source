from crispy_forms.layout import Button


class DynamicFormsetButton(Button):
    """
    Creates a button used to dynamically add more forms to a formset,
    through `common/forms/dynamic_formset.js`.
    The button is styled to set it apart from other components in the form.
    """

    def __init__(self, button_text, **kwargs):
        super().__init__("Add form", button_text, data_formset_add_form=True, **kwargs)
        self.field_classes = "btn btn-secondary d-block mb-3"
