from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, HiddenInput, ValidationError

from accounts.models import UserCustom
from common.embeddable_text.templatetags.embeddable_text import get_embeddable_text


class LoginForm(AuthenticationForm):
    """Form used for logging in."""

    next = CharField(widget=HiddenInput, required=False)

    helper = FormHelper()
    helper.form_action = "login"
    helper.add_input(Submit("submit", "Logg inn"))

    def __init__(self, autofocus=True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autofocus"] = autofocus

    def confirm_login_allowed(self, user):
        if user.membership_status == UserCustom.MembershipStatus.INACTIVE:
            raise ValidationError(
                get_embeddable_text("Inaktiv brukar"),
                code="inactive",
            )
