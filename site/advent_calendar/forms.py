from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import AdventCalendar, Window


class AdventCalendarForm(forms.ModelForm):
    """Form for creating an advent calendar."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag julekalender"))

    class Meta:
        model = AdventCalendar
        fields = ["year"]


class WindowCreateForm(forms.ModelForm):
    """Form for creating a window."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg ut luke"))

    def __init__(self, advent_calendar=None, *args, **kwargs):
        if advent_calendar:
            self.helper.form_action = reverse(
                "advent_calendar:window_create",
                args=[advent_calendar.year],
            )
        super().__init__(*args, **kwargs)

    class Meta:
        model = Window
        fields = ["title", "content", "index"]
        widgets = {"index": forms.HiddenInput()}


class WindowUpdateForm(forms.ModelForm):
    """Form for updating a window."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Rediger luke"))

    class Meta:
        model = Window
        fields = ["title", "content"]
