from django.forms import (
    DateInput,
    MultiWidget,
    Select,
    SelectMultiple,
    SplitDateTimeWidget,
    TimeInput,
)


class DateDateInput(DateInput):
    """
    DateInput with `type` set to `date`.
    Displays a date-picker in supporting browsers.
    """

    def __init__(self, attrs=None, format=None):
        attrs = {"type": "date", **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class SplitDateTimeWidgetCustom(SplitDateTimeWidget):
    """
    Date/time widget with custom styling and date-picker.
    Must be used with `django.forms.SplitDateTimeField`.
    """

    template_name = "common/forms/split_datetime_custom.html"

    def __init__(self, attrs=None):
        widgets = [DateDateInput(), TimeInput(format="%H:%M")]
        MultiWidget.__init__(self, widgets, attrs)


class AutocompleteSelect(Select):
    class Media:
        js = ("common/forms/autocomplete_select.js",)


class AutocompleteSelectMultiple(SelectMultiple):
    class Media:
        js = ("common/forms/autocomplete_select.js",)
