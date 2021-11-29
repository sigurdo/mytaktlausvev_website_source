from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Julekalender, Window


class AdventCalendarForm(forms.ModelForm):
    """Form for creating an advent calendar."""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lag julekalender"))

    class Meta:
        model = Julekalender
        fields = ["year"]


class WindowCreateForm(forms.ModelForm):
    """Form for creating a window."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg ut luke"))

    def __init__(self, action=None, *args, **kwargs):
        self.helper.form_action = action
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
