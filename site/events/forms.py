"""Forms for the "events"-app."""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from common.widgets import SplitDateTimeWidgetCustom
from .models import Event, EventAttendance


class EventForm(forms.ModelForm):
    """Form for creating and editing events."""

    start_time = forms.SplitDateTimeField(
        label="Starttid", widget=SplitDateTimeWidgetCustom()
    )
    end_time = forms.SplitDateTimeField(
        label="Sluttid", widget=SplitDateTimeWidgetCustom(), required=False
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger hending"))

    class Meta:
        model = Event
        fields = ["title", "start_time", "end_time", "content"]


class EventAttendanceForm(forms.ModelForm):
    """Form for registering event attendance."""

    helper = FormHelper()
    helper.field_class = "col-lg-4"
    helper.add_input(Submit("submit", "Registrer"))

    class Meta:
        model = EventAttendance
        fields = ["status"]
