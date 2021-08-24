from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(AuthenticationForm):
    """Form used for logging in."""

    helper = FormHelper()
    helper.form_tag = False
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-8 form-field"
    helper.add_input(Submit("submit", "Logg inn"))
