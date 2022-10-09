from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import (
    BooleanField,
    ChoiceField,
    Form,
    ModelForm,
    TextInput,
    modelformset_factory,
)

from accounts.models import UserCustom
from common.forms.layouts import DynamicFormsetButton
from common.forms.widgets import AutocompleteSelect

from .models import Jacket


class JacketForm(ModelForm):
    """Form for creating and/or updating a jacket."""

    class Meta:
        model = Jacket
        fields = [
            "number",
            "location",
            "user",
            "comment",
            "state_comment",
            
            "state",
            
        ]
        widgets = {
            "comment": TextInput,
            "state_comment": TextInput,
            "user": AutocompleteSelect}


class JacketsFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(DynamicFormsetButton("Legg til endå ein jakke"))
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/forms/table_inline_formset_shade_delete.html"


JacketsFormset = modelformset_factory(
    Jacket,
    form=JacketForm,
    can_delete=True,
    extra=1,
)


JacketsFormset.helper = JacketsFormsetHelper()


