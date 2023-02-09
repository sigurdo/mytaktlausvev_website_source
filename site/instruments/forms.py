from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, TextInput, modelformset_factory

from common.forms.layouts import DynamicFormsetButton
from common.forms.widgets import AutocompleteSelect

from .models import Instrument


class InstrumentForm(ModelForm):
    """Form for creating and/or updating instruments."""

    class Meta:
        model = Instrument
        fields = [
            "type",
            "identifier",
            "user",
            "location",
            "serial_number",
            "comment",
            "state",
        ]
        widgets = {
            "type": AutocompleteSelect,
            "user": AutocompleteSelect,
            "comment": TextInput,
        }


class InstrumentFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(DynamicFormsetButton("Legg til endå eit instrument"))
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/forms/table_inline_formset_shade_delete.html"


InstrumentFormset = modelformset_factory(
    Instrument,
    form=InstrumentForm,
    can_delete=True,
    extra=1,
)

InstrumentFormset.helper = InstrumentFormsetHelper()
