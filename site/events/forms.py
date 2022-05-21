from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    TEMPLATE_PACK,
    Fieldset,
    Layout,
    LayoutObject,
    Submit,
)
from django.forms import (
    ModelForm,
    NumberInput,
    SplitDateTimeField,
    TextInput,
    inlineformset_factory,
)
from django.template.loader import render_to_string
from django.utils.timezone import now

from common.widgets import SplitDateTimeWidgetCustom

from .models import Event, EventAttendance, EventTldrEntry


class EventTldrFormsetLayoutObject(LayoutObject):
    """
    Boiled from https://stackoverflow.com/questions/15157262/django-crispy-forms-nesting-a-formset-within-a-form

    Layout object. It renders an entire formset, as though it was a Field.
    """

    template = "common/table_inline_formset_shade_delete.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context

        # crispy_forms/layout.py:302 requires us to have a fields property
        self.fields = []

        # Overrides class variable with an instance level variable
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {"wrapper": self, "formset": formset})


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
            EventTldrFormsetLayoutObject("formset"),
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
