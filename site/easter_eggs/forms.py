from django import forms
from django.forms import ChoiceField, CharField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BrewForm(forms.Form):
    drink = ChoiceField(choices=[("coffee", "Kaffe")], label="Drikke")
    addition = CharField(label="Tilsetjing", required=False)
    helper = FormHelper()
    helper.add_input(Submit("submit", "Brygg"))
