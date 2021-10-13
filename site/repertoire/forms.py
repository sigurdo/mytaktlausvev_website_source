"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.forms import formset_factory, modelformset_factory, widgets
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