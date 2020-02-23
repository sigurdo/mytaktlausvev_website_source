from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from julekalender.models import Julekalender


class NewJulekalenderForm(forms.ModelForm):
    """Form for creating a new julekalender"""

    helper = FormHelper()
    helper.form_id = "newJulekalender"
    helper.form_method = "post"
    helper.form_action = "julekalender/new"
    helper.add_input(Submit("submit", "Ny julekalender"))

    class Meta:
        model = Julekalender
        fields = ["year"]
        labels = {"year": "År"}
