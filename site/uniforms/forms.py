from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, TextInput, modelformset_factory

from .models import Jacket


class JacketUpdateForm(ModelForm):
    """Form for updating a Jacket"""

    class Meta:
        model = Jacket
        fields = [
            "number",
            "state",
            "location",
            "owner",
            "comment",
        ]
        widgets = {"comment": TextInput}


class JacketsUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


JacketsUpdateFormset = modelformset_factory(
    Jacket,
    form=JacketUpdateForm,
    can_delete=True,
    extra=5,
)


JacketsUpdateFormset.helper = JacketsUpdateFormsetHelper()
