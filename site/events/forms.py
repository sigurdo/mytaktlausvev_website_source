"""Forms for the "events"-app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Event


class CreateEventForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "event_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-6 form-field"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Event
        exclude = ["owner"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime"}),
            "description": forms.Textarea(),
        }
