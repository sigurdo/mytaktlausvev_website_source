from .models import Song
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SongForm(forms.ModelForm):
    """Form for creating and editing songs."""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lag/endre sang"))

    class Meta:
        model = Song
        fields = ["title", "content"]
