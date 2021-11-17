from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ButtonsForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), label="Motiv"
    )
    num_of_each = forms.IntegerField(min_value=1, max_value=64, initial=1, label="Antal skiltmerke av kvart motiv")
    button_diameter_mm = forms.IntegerField(min_value=10, max_value=200, initial=67, label="Diameter for kvart skiltmerke i mm")

    helper = FormHelper()
    helper.add_input(Submit("submit" ,"Generer PDF"))
