"""Forms for the 'salvage_diary'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import CharField, HiddenInput, ModelForm

from accounts.models import UserCustom
from common.forms.widgets import AutocompleteSelectMultiple, DateDateInput
from salvage_diary.models import Mascot, SalvageDiaryEntry


class MascotForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["creators"].queryset = UserCustom.objects.exclude(
            membership_status=UserCustom.MembershipStatus.INACTIVE
        )

    class Meta:
        model = Mascot
        fields = [
            "name",
            "image",
            "creationStartDate",
            "creationEndDate",
            "password",
            "creators",
            "note",
        ]
        widgets = {
            "creators": AutocompleteSelectMultiple,
            "creationStartDate": DateDateInput,
            "creationEndDate": DateDateInput,
        }


class SalvageDiaryEntryForm(ModelForm):
    password = CharField(
        label="Passord",
        help_text="Dette finner dykk eit stad på maskoten.",
    )
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    def __init__(self, mascot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["mascot"] = mascot
        self.fields["mascot"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        mascot = cleaned_data.get("mascot")
        mascotPassword = Mascot.objects.get(name=mascot).password

        if password != mascotPassword:
            raise ValidationError(
                "Passordet matcher ikke. Obs! Bilde må lastes opp igjen",
                code="invalid",
            )

    class Meta:
        model = SalvageDiaryEntry
        fields = ["title", "thieves", "image", "story", "event", "mascot"]
        widgets = {
            "mascot": HiddenInput,
        }
