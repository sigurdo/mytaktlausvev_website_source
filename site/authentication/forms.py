from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, HiddenInput
from django.urls.base import reverse_lazy


class LoginForm(AuthenticationForm):
    """Form used for logging in."""

    next = CharField(widget=HiddenInput, required=False)

    helper = FormHelper()
    helper.field_class = "col-lg-8"
    helper.form_action = reverse_lazy("login")
    helper.add_input(Submit("submit", "Logg inn"))
