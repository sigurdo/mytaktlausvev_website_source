from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import (
    BooleanField,
    ChoiceField,
    Form,
    ModelForm,
    TextInput,
    modelformset_factory,
)

from accounts.models import UserCustom
from common.forms.layouts import DynamicFormsetButton
from common.forms.widgets import AutocompleteSelect

from .models import Jacket


class JacketForm(ModelForm):
    """Form for creating and/or updating a jacket."""

    class Meta:
        model = Jacket
        fields = [
            "number",
            "location",
            "comment",
            "state",
        ]
        widgets = {"comment": TextInput}


class JacketsFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(DynamicFormsetButton("Legg til endå ein jakke"))
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/forms/table_inline_formset_shade_delete.html"


JacketsFormset = modelformset_factory(
    Jacket,
    form=JacketForm,
    can_delete=True,
    extra=1,
)


JacketsFormset.helper = JacketsFormsetHelper()


class AddJacketUserForm(Form):
    def user_choices():
        """Returns a list of choice tuples for all users in the database."""
        users = UserCustom.objects.all()
        return [(user.pk, str(user)) for user in users]

    def validator_user_does_not_have_jacket(user_pk):
        """Validates that a user does not already have a jacket."""
        user = UserCustom.objects.get(pk=user_pk)
        jacket = user.get_jacket()
        if jacket:
            raise ValidationError(
                f"{str(user).capitalize()} har allereie {str(jacket).lower()}"
            )

    def clean(self):
        """Validate that the jacket does not already have an owner if set_owner=True."""
        cleaned_data = super().clean()
        set_owner = cleaned_data["set_owner"]
        if set_owner and self.jacket.jacket_users.filter(is_owner=True).exists():
            self.add_error(
                "set_owner", ValidationError(f"{self.jacket} har allereie ein eigar")
            )
        return cleaned_data

    user = ChoiceField(
        label="Brukar",
        choices=user_choices,
        validators=[validator_user_does_not_have_jacket],
        widget=AutocompleteSelect,
    )
    set_owner = BooleanField(label="Sett som eigar", required=False, initial=True)

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre"))


class RemoveJacketUserForm(Form):
    transfer_ownership = BooleanField(
        label="Om brukaren var eigar, finn ein ny eigar fra ekstrabrukarane automatisk",
        required=False,
        initial=True,
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Fjern", css_class="btn-danger"))
