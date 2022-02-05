from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import DateInput, ModelForm

from .models import Minutes


class MinutesForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre referat"))

    class Meta:
        model = Minutes
        fields = ["title", "date", "content", "file"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
        }
