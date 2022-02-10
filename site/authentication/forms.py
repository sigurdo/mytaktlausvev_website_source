from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, HiddenInput


class LoginForm(AuthenticationForm):
    """Form used for logging in."""

    next = CharField(widget=HiddenInput, required=False)

    helper = FormHelper()
    helper.form_action = "login"
    helper.add_input(Submit("submit", "Logg inn"))
