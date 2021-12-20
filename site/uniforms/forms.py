from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    BooleanField,
    ChoiceField,
    Form,
    ModelForm,
    TextInput,
    modelformset_factory,
)

from accounts.models import UserCustom

from .models import Jacket


class JacketUpdateForm(ModelForm):
    """Form for updating a Jacket"""

    class Meta:
        model = Jacket
        fields = [
            "number",
            "state",
            "location",
            "owner",
            "comment",
        ]
        widgets = {"comment": TextInput}


class JacketsUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


JacketsUpdateFormset = modelformset_factory(
    Jacket,
    form=JacketUpdateForm,
    can_delete=True,
    extra=5,
)


JacketsUpdateFormset.helper = JacketsUpdateFormsetHelper()


class AddJacketUserForm(Form):
    def user_choices():
        users = UserCustom.objects.all()
        return [(user.pk, str(user)) for user in users]

    user = ChoiceField(label="Brukar", choices=user_choices)
    set_owner = BooleanField(label="Sett som eigar", required=False, initial=True)
    remove_old_ownerships = BooleanField(
        label="Fjern gamle eigarskap", required=False, initial=True
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre"))


class RemoveJacketUserForm(Form):
    remove_owner = BooleanField(label="Fjern eigarskap", required=False, initial=True)

    helper = FormHelper()
    helper.add_input(Submit("submit", "Fjern", css_class="btn btn-danger"))
