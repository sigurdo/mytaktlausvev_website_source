from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Julekalender, Window


class CalendarForm(forms.ModelForm):
    """Form for creating a calendar."""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lag julekalender"))

    class Meta:
        model = Julekalender
        fields = ["year"]


class WindowForm(forms.ModelForm):
    """Form for creating a window."""

    helper = FormHelper()
    helper.form_action = "window_create"
    helper.add_input(Submit("submit", "Legg ut"))

    class Meta:
        model = Window
        fields = ["title", "content", "calendar", "index"]
        widgets = {"calendar": forms.HiddenInput(), "index": forms.HiddenInput()}
