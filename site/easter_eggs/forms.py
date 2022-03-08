from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import CharField, ChoiceField


class BrewForm(forms.Form):
    drink = ChoiceField(choices=[("coffee", "Kaffe"), ("tea", "Te")], label="Drikk")
    addition = CharField(label="Tilsetjing", required=False)
    helper = FormHelper()
    helper.add_input(Submit("submit", "Brygg"))
