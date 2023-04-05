"""Forms for the 'salvage_diary'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import CharField, HiddenInput, ModelForm

from accounts.models import UserCustom
from common.forms.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
    DateDateInput,
)
from salvage_diary.models import (
    Mascot,
    SalvageDiaryEntryExternal,
    SalvageDiaryEntryInternal,
)


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
            "creation_start_date",
            "creation_end_date",
            "password",
            "creators",
            "note",
        ]
        widgets = {
            "creators": AutocompleteSelectMultiple,
            "creation_start_date": DateDateInput,
            "creation_end_date": DateDateInput,
        }


class SalvageDiaryEntryExternalForm(ModelForm):
    password = CharField(
        label="Passord",
        help_text="Dette finn dykk ein stad på maskoten.",
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
        mascot_password = Mascot.objects.get(name=mascot).password

        if password != mascot_password:
            raise ValidationError(
                "Passordet er feil. Obs! Bilete må lastast opp igjen.",
                code="invalid",
            )

    class Meta:
        model = SalvageDiaryEntryExternal
        fields = ["title", "thieves", "event", "image", "story", "mascot"]
        widgets = {
            "mascot": HiddenInput,
        }


class SalvageDiaryEntryExternalUpdateForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    class Meta:
        model = SalvageDiaryEntryExternal
        fields = ["title", "thieves", "event", "image", "story"]


class SalvageDiaryEntryInternalForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    class Meta:
        model = SalvageDiaryEntryInternal
        fields = ["title", "item", "thieves", "users", "event", "image", "story"]
        widgets = {
            "event": AutocompleteSelect,
            "users": AutocompleteSelectMultiple,
        }
