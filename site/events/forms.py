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

from common.forms.layouts import DynamicFormsetButton, FormsetLayoutObject
from common.forms.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
    SplitDateTimeWidgetCustom,
)

from .models import Event, EventAttendance, EventKeyinfoEntry


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
        "category",
        "start_time",
        "end_time",
        "location",
        "location_map_link",
        Fieldset(
            "Nykelinfo",
            HTML(
                """
                {% load embeddable_text markdown %}
                {% get_embeddable_text "Nykelinfo-hjelpetekst for hendingar" as text %}
                {{ text | markdown }}
                """
            ),
            FormsetLayoutObject(),
        ),
        "content",
        Fieldset(
            "Repertoar",
            "include_active_repertoires",
            "repertoires",
            "extra_scores",
        ),
        "gallery",
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "category",
            "start_time",
            "end_time",
            "content",
            "location",
            "location_map_link",
            "include_active_repertoires",
            "repertoires",
            "extra_scores",
            "gallery",
        ]
        widgets = {
            "category": AutocompleteSelect,
            "repertoires": AutocompleteSelectMultiple,
            "extra_scores": AutocompleteSelectMultiple,
            "gallery": AutocompleteSelect,
        }


class EventAttendanceForm(ModelForm):
    """Form for registering event attendance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = "col-lg-4"
        self.helper.add_input(Submit("submit", "Send svar"))

    class Meta:
        model = EventAttendance
        fields = ["status", "instrument_type"]
        widgets = {
            "instrument_type": AutocompleteSelect,
        }


class EventKeyinfoEntryForm(ModelForm):
    """Form for updating a keyinfo entry."""

    class Meta:
        model = EventKeyinfoEntry
        fields = ["key", "info", "order"]
        help_texts = {"order": ""}
        widgets = {
            "key": TextInput(attrs={"size": 8}),
            "order": NumberInput(attrs={"size": 4}),
        }


EventKeyinfoEntryFormset = inlineformset_factory(
    Event,
    EventKeyinfoEntry,
    form=EventKeyinfoEntryForm,
    extra=1,
)


class EventKeyinfoEntryFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input(DynamicFormsetButton("Legg til endå ein nykelinfo"))
        self.template = "common/forms/table_inline_formset_shade_delete.html"


EventKeyinfoEntryFormset.helper = EventKeyinfoEntryFormsetHelper()
