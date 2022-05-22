from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django.forms import (
    ModelForm,
    NumberInput,
    SplitDateTimeField,
    TextInput,
    inlineformset_factory,
)
from django.utils.timezone import now

from common.forms import FormsetLayoutObject
from common.widgets import SplitDateTimeWidgetCustom

from .models import Event, EventAttendance, EventTldrEntry


class EventForm(ModelForm):
    """Form for creating and editing events."""

    start_time = SplitDateTimeField(
        label="Starttid", widget=SplitDateTimeWidgetCustom(), initial=now
    )
    end_time = SplitDateTimeField(
        label="Sluttid", widget=SplitDateTimeWidgetCustom(), required=False
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre hending"))
    helper.layout = Layout(
        "title",
        "start_time",
        "end_time",
        Fieldset(
            "TL;DR",
            HTML(
                """
                {% load embeddable_text markdown %}
                {% get_embeddable_text "Hjelpetekst TL;DR-seksjon for hendingar" as text %}
                {{ text | markdown }}
                """
            ),
            FormsetLayoutObject("formset"),
        ),
        "content",
    )

    class Meta:
        model = Event
        fields = ["title", "start_time", "end_time", "content"]


class EventAttendanceForm(ModelForm):
    """Form for registering event attendance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = "col-lg-4"
        self.helper.add_input(Submit("submit", "Send svar"))

    class Meta:
        model = EventAttendance
        fields = ["status"]


class EventTldrEntryForm(ModelForm):
    """Form for updating a TL;DR entry."""

    class Meta:
        model = EventTldrEntry
        fields = ["key", "value", "order"]
        help_texts = {"order": ""}
        widgets = {
            "key": TextInput(attrs={"size": 8}),
            "order": NumberInput(attrs={"size": 4}),
        }


EventTldrEntryFormset = inlineformset_factory(
    Event,
    EventTldrEntry,
    form=EventTldrEntryForm,
    extra=5,
)
