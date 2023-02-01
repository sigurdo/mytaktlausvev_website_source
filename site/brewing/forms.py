from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django.forms import HiddenInput, ModelForm, NumberInput

from .models import Brew, Transaction, TransactionType


class BrewForm(ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            "Generelt", "name", "price_per_liter", "available_for_purchase", "logo"
        ),
        Fieldset(
            "Brygging",
            "OG",
            "FG",
        ),
        Submit("submit", "Lagre brygg"),
    )

    class Meta:
        model = Brew
        fields = [
            "name",
            "price_per_liter",
            "available_for_purchase",
            "logo",
            "OG",
            "FG",
        ]


class DepositForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn pengar"))
    helper.layout = Layout(
        HTML(
            """
                {% load embeddable_text markdown %}
                {% get_embeddable_text "Innbetaling til bryggjekassa" as text %}
                {{ text | markdown }}
                """
        ),
        "price",
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["user"] = user
        self.initial["type"] = TransactionType.DEPOSIT
        self.fields["user"].disabled = True
        self.fields["type"].disabled = True

    class Meta:
        model = Transaction
        fields = ["price", "user", "type"]
        widgets = {
            "price": NumberInput(attrs={"min": 1}),
            "user": HiddenInput,
            "type": HiddenInput,
        }


class BrewPurchaseForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Kjøp"))

    def __init__(self, user, brew: Brew, size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial["user"] = user
        self.initial["price"] = -(
            brew.price_per_0_5()
            if size == Brew.Sizes.SIZE_0_5
            else brew.price_per_0_33()
        )
        self.initial["brew"] = brew
        self.initial["type"] = TransactionType.PURCHASE
        self.fields["user"].disabled = True
        self.fields["price"].disabled = True
        self.fields["brew"].disabled = True
        self.fields["type"].disabled = True

    class Meta:
        model = Transaction
        fields = ["price", "brew", "user", "type"]
        widgets = {
            "price": HiddenInput,
            "brew": HiddenInput,
            "user": HiddenInput,
            "type": HiddenInput,
        }
