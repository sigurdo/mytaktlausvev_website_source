from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ClearableFileInput, Form, ImageField, IntegerField, ModelForm

from .models import ButtonDesign


class ButtonsForm(Form):
    images = ImageField(
        widget=ClearableFileInput(attrs={"multiple": True}), label="Motiv"
    )
    num_of_each = IntegerField(
        min_value=1, max_value=64, initial=1, label="Antal buttons av kvart motiv"
    )
    button_visible_diameter_mm = IntegerField(
        min_value=10,
        max_value=100,
        initial=57,
        label="Synleg diameter for kvar button i mm",
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Generer PDF"))


class ButtonDesignForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre buttonmotiv"))

    class Meta:
        model = ButtonDesign
        fields = ["name", "image"]
