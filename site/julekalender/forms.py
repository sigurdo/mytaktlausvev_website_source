from django import forms
from julekalender.models import Julekalender


class NewJulekalenderForm(forms.ModelForm):
    """Form for creating a new julekalender"""

    class Meta:
        model = Julekalender
        fields = ["year"]
        labels = {"year": "År"}
