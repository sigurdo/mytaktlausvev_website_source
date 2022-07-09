from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class ButtonsForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), label="Motiv"
    )
    num_of_each = forms.IntegerField(
        min_value=1, max_value=64, initial=1, label="Antal buttons av kvart motiv"
    )
    button_diameter_mm = forms.IntegerField(
        min_value=10,
        max_value=100,
        initial=57,
        label="Synleg diameter for kvar button i mm",
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Generer PDF"))
