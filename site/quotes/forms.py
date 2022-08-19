"""Forms for the 'quotes'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from quotes.models import Quote


class QuoteForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg inn"))

    class Meta:
        model = Quote
        fields = ["quote", "context"]
