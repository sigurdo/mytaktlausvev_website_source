from django.forms import ModelForm, modelformset_factory, TextInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Instrument


class InstrumentUpdateForm(ModelForm):
    """Form for creating a repertoire entry"""

    class Meta:
        model = Instrument
        fields = [
            "name",
            "type",
            "user",
            "location",
            "serial_number",
            "comment",
            "state",
        ]
        widgets = {"comment": TextInput}


class InstrumentUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


InstrumentUpdateFormset = modelformset_factory(
    Instrument,
    form=InstrumentUpdateForm,
    extra=1,
)

InstrumentUpdateFormset.helper = InstrumentUpdateFormsetHelper()
