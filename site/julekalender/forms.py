from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from julekalender.models import Julekalender
from julekalender.models import Window


class NewJulekalenderForm(forms.ModelForm):
    """Form for creating a new julekalender"""

    class Meta:
        model = Julekalender
        fields = ["year"]
        labels = {"year": "År"}


class NewWindowForm(forms.ModelForm):
    """Form for posting a new window"""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Legg ut"))

    class Meta:
        model = Window
        fields = ["title", "post"]
        widgets = {"post": forms.Textarea()}
        labels = {"title": "Tittel"}
