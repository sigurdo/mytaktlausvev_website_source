from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from contact.models import ContactCategory


class ContactForm(forms.Form):
    """Form for contacting the board."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Send melding"))

    name = forms.CharField(label="Namnet ditt", max_length=255)
    email = forms.EmailField(label="E-postadressa di")
    subject = forms.CharField(label="Emne", max_length=255)
    category = forms.ModelChoiceField(
        label="Kategori",
        queryset=ContactCategory.objects.all(),
        to_field_name="name",
        empty_label=None,
        required=True,
    )
    message = forms.CharField(label="Melding", max_length=5000, widget=forms.Textarea)
    send_to_self = forms.BooleanField(
        label="Send ein kopi til deg sjølv", required=False
    )
