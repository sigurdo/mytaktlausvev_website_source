"""Forms for the 'sheetmusic'-app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, HTML

from . import models

class RepertoireCreateForm(forms.ModelForm):
    """Form for creating a new repertoire"""
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = models.Repertoire
        fields = ["title"]
        labels = {
            "title": "Tittel"
        }

class RepertoireUpdateForm(forms.ModelForm):
    """ Form for editing a repertoire """
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = models.Repertoire
        fields = ["title"]
        labels = {
            "title": "Tittel"
        }

class RepertoireEntryCreateForm(forms.ModelForm):
    """ Form for creating a repertoire entry """
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = models.RepertoireEntry
        fields = ["score"]
        labels = {
            "score": "Note"
        }
