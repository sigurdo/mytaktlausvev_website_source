from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.form_id = "login_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-8 form-field"
    helper.add_input(Submit("submit", "Logg inn"))