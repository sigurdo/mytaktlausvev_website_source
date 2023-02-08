from urllib.parse import urlencode

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import BooleanField, Form, ModelForm, ModelMultipleChoiceField
from django.urls import reverse

from common.constants.models import Constant
from common.forms.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
    DateDateInput,
)

from .models import UserCustom


class UserCustomCreateForm(UserCreationForm):
    no_storage_access = BooleanField(
        label="Eg forstår at eg ikkje får tilgjenge til lageret "
        "utan å legge inn studentkortnummeret mitt.",
        required=False,
    )

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
        ),
        Fieldset(
            "Lagertilgjenge",
            HTML(
                '<p class="col-lg-6">Me treng studentkortnummeret ditt '
                "for å gje deg tilgjenge til lageret vårt. "
                "Om du ikkje har studentkortet ditt no "
                "kan du legge det inn seinare.</p>"
            ),
            "student_card_number",
            "no_storage_access",
        ),
        Fieldset("Taktlaus-ting", "instrument_type", "membership_period"),
        Submit("submit", "Lag brukar"),
    )

    def __init__(self, *args, **kwargs):
        """
        Require all fields except `student_card_number` and `no_storage_access`.
        These are handled separately.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "student_card_number" or field_name == "no_storage_access":
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

    def clean_no_storage_access(self) -> bool:
        """
        Should require `no_storage_access`
        if no student card number is provided.
        """
        student_card_number = self.cleaned_data["student_card_number"]
        no_storage_access = self.cleaned_data["no_storage_access"]
        if not no_storage_access and not student_card_number:
            raise ValidationError(
                "Feltet er påkrevd om du ikkje legg inn studentkortnummer."
            )

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
        widgets = {"birthdate": DateDateInput, "instrument_type": AutocompleteSelect}


class UserCustomUpdateForm(ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset("Brukar", "email", "avatar"),
        Fieldset(
            "Personleg",
            "name",
            "phone_number",
            "birthdate",
            "address",
            "home_page",
            "student_card_number",
        ),
        Fieldset("Taktlaus-ting", "instrument_type", "membership_period"),
        Fieldset("Kalenderintegrasjon", "calendar_feed_start_date"),
        Fieldset("Anna", "light_mode", "image_sharing_consent", "orchestras"),
        Submit("submit", "Lagre brukar"),
    )

    class Meta:
        model = UserCustom
        fields = [
            "email",
            "avatar",
            "name",
            "phone_number",
            "birthdate",
            "address",
            "home_page",
            "student_card_number",
            "instrument_type",
            "membership_period",
            "light_mode",
            "image_sharing_consent",
            "calendar_feed_start_date",
            "orchestras",
        ]
        widgets = {
            "birthdate": DateDateInput,
            "instrument_type": AutocompleteSelect,
            "calendar_feed_start_date": DateDateInput,
            "orchestras": AutocompleteSelectMultiple,
        }


class ImageSharingConsentForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Send inn svar"))

    def __init__(self, next_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_action = reverse("accounts:ImageSharingConsentUpdate")
        if next_url:
            self.helper.form_action += f"?{urlencode({'next': next_url})}"

    class Meta:
        model = UserCustom
        fields = ["image_sharing_consent"]
        help_texts = {"image_sharing_consent": ""}


class InstrumentGroupLeadersForm(Form):
    instrument_group_leaders = ModelMultipleChoiceField(
        queryset=UserCustom.objects.all(),
        label="Instrumentgruppeleiarar",
        widget=AutocompleteSelectMultiple,
        required=False,
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre instrumentgruppeleiarar"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instrument_group_leader_group_name, _ = Constant.objects.get_or_create(
            name="Instrumentgruppeleiargruppenamn"
        )
        self.instrument_leaders_group, _ = Group.objects.get_or_create(
            name=instrument_group_leader_group_name.value
        )
        self.fields[
            "instrument_group_leaders"
        ].initial = self.instrument_leaders_group.user_set.all()

    def save(self):
        self.instrument_leaders_group.user_set.set(
            self.data.getlist("instrument_group_leaders")
        )
