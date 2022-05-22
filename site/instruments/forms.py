from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, TextInput, modelformset_factory

from common.forms import DynamicFormsetButton

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
        widgets = {"comment": TextInput}


class InstrumentFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(DynamicFormsetButton("Legg til enda eit instrument"))
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


InstrumentFormset = modelformset_factory(
    Instrument,
    form=InstrumentForm,
    can_delete=True,
    extra=1,
)

InstrumentFormset.helper = InstrumentFormsetHelper()
