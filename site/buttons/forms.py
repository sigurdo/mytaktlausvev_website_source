from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ClearableFileInput, Form, ImageField, IntegerField, ModelForm

from .models import ButtonDesign


class ButtonsForm(Form):
    images = ImageField(
        widget=ClearableFileInput(attrs={"multiple": True}),
        label="Motiv (du kan laste opp fleire samstundes!)",
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
    button_backside_padding_mm = IntegerField(
        min_value=0,
        max_value=100,
        initial=5,
        label="Tjukn på baksidepolstring i mm",
        help_text="Kor tjukk polstringa (padding) på baksida skal vere. Denne avstanden må vere rekna inn i motivet du lastar opp.",
    )
    button_minimum_distance_mm = IntegerField(
        min_value=0,
        max_value=100,
        initial=0,
        label="Minste avstand millom kvar button i mm",
    )
    paper_margin_mm = IntegerField(
        min_value=0,
        max_value=100,
        initial=3,
        label="Papirmarg i mm",
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Generer PDF"))


class ButtonDesignForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre buttonmotiv"))

    class Meta:
        model = ButtonDesign
        fields = ["name", "image", "public"]
