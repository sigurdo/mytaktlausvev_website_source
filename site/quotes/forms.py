"""Forms for the 'quotes'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from common.forms.widgets import AutocompleteSelectMultiple
from quotes.models import Quote


class QuoteForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    def clean(self):
        cleaned_data = super().clean()
        users = cleaned_data.get("users")
        quoted_as = cleaned_data.get("quoted_as")

        if not users and not quoted_as:
            raise ValidationError(
                'Du må fylle inn anten "Medlem som vert sitert" eller "Sitert som".',
                code="invalid",
            )

    class Meta:
        model = Quote
        fields = ["quote", "users", "quoted_as"]
        widgets = {"users": AutocompleteSelectMultiple}
