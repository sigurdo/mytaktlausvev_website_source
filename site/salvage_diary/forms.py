"""Forms for the 'salvage_diary'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import CharField, HiddenInput, ModelForm

from accounts.models import UserCustom
from common.forms.widgets import AutocompleteSelectMultiple, DateDateInput
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("creationStartDate")
        end_date = cleaned_data.get("creationEndDate")

        if start_date and end_date and start_date > end_date:
            raise ValidationError(
                """Så vidt me veit er tidsreiser enno ikkje offentleg tilgjengeleg, så startdatoen kan ikkje vera etter sluttdatoen. 
                Viss du kan reisa i tid, ver vennleg og gi beskjed til vevkom slik at me kan fjerna valideringa.""",
                code="invalid",
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


class SalvageDiaryEntryExternalForm(ModelForm):
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
        fields = ["title", "item", "thieves", "event", "image", "story"]
