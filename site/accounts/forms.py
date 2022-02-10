from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from common.widgets import DateDateInput

from .models import UserCustom


class UserCustomCreateForm(UserCreationForm):
    helper = FormHelper()
    helper.field_class = "col-lg-6"
    helper.layout = Layout(
        Fieldset("Brukar", "username", "email", "password1", "password2"),
        Fieldset(
            "Personleg",
            "name",
            "phone_number",
            "birthdate",
            "address",
            "student_card_number",
        ),
        Fieldset("Taktlaus-ting", "instrument_type", "membership_period"),
        Submit("submit", "Lag brukar"),
    )

    def __init__(self, *args, **kwargs):
        """
        Require all fields except `student_card_number`.
        Not everyone has their student card with them.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "student_card_number":
                continue
            field.required = True

    def clean_username(self) -> str:
        """
        Validate that no user exists with the same username, case-insensitive.
        Model forms do not automatically validate functional unique constraints.
        """
        username = self.cleaned_data["username"]
        if UserCustom.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                "Det eksisterar allereie ein brukar med dette brukarnamnet.",
                code="unique",
            )

        return username

    class Meta(UserCreationForm.Meta):
        model = UserCustom
        fields = UserCreationForm.Meta.fields + (
            "email",
            "name",
            "phone_number",
            "address",
            "birthdate",
            "student_card_number",
            "instrument_type",
            "membership_period",
        )
        widgets = {"birthdate": DateDateInput}


class UserCustomUpdateForm(ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset("Brukar", "email"),
        Fieldset(
            "Personleg",
            "name",
            "phone_number",
            "birthdate",
            "address",
            "student_card_number",
        ),
        Fieldset("Taktlaus-ting", "instrument_type", "membership_period"),
        Submit("submit", "Rediger brukar"),
    )

    class Meta:
        model = UserCustom
        fields = [
            "email",
            "name",
            "phone_number",
            "birthdate",
            "address",
            "student_card_number",
            "instrument_type",
            "membership_period",
        ]
        widgets = {"birthdate": DateDateInput}
