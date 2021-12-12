from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Gallery


class GalleryForm(forms.ModelForm):
    """Form for creating and editing galleries."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger galleri"))

    class Meta:
        model = Gallery
        fields = ["title", "date", "date_to", "content"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "date_to": forms.DateInput(attrs={"type": "date"}),
        }
