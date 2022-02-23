from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django.forms import (
    CharField,
    EmailField,
    Form,
    HiddenInput,
    ModelChoiceField,
    Textarea,
    TextInput,
)

from contact.models import ContactCategory


class ContactForm(Form):
    """Form for contacting the board."""

    helper = FormHelper()
    helper.field_class = "col-lg-8"
    helper.layout = Layout(
        Field("name"),
        Field("email"),
        Field("subject"),
        Div(
            Field("content", tabindex=-1), css_class="visually-hidden", aria_hidden=True
        ),
        Field("category"),
        Field("message"),
        Submit("submit", "Send melding"),
    )

    name = CharField(label="Namnet ditt", max_length=255)
    email = EmailField(label="E-postadressa di")
    subject = CharField(label="Emne", max_length=255)
    category = ModelChoiceField(
        label="Kategori",
        queryset=ContactCategory.objects.all(),
        to_field_name="name",
        empty_label=None,
        required=True,
    )
    message = CharField(label="Melding", max_length=5000, widget=Textarea)

    # Field used for spam detection
    content = CharField(label="Innhald", required=False, widget=Textarea)
