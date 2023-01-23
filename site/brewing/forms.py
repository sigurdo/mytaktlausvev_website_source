from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import HiddenInput, ModelForm, NumberInput

from .models import Transaction, TransactionType


class DepositForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn pengar"))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["user"] = user
        self.initial["type"] = TransactionType.DEPOSIT
        self.fields["user"].disabled = True
        self.fields["type"].disabled = True

    class Meta:
        model = Transaction
        fields = ["price", "comment", "user", "type"]
        widgets = {
            "price": NumberInput(attrs={"min": 1}),
            "user": HiddenInput,
            "type": HiddenInput,
        }
