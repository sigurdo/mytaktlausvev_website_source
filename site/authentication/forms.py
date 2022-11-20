from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, HiddenInput, ValidationError

from accounts.models import UserCustom


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
                "Du har ikkje betalt medlemskontingent for Dei Taktlause. Du har difor fått status som inaktiv, fordi du har vore medlem i mindre enn 2 år. Hvis du har lånt instrument, jakke, eller anna materiale frå Dei Taktlause, lever det attende. Du har mista tilgjenge til veven, Discord, og alle hendingar. Ta kontakt med styret om du vil vere pensjonist for å behalde tilgjenge, om dette er feil og du fortsatt er aktiv, eller om du har spørsmål.",
                code="inactive",
            )
