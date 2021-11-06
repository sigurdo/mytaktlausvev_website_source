from django import forms


class DateDateInput(forms.DateInput):
    """
    DateInput with `type` set to `date`.
    Displays a date-picker in supporting browsers.
    """

    def __init__(self, attrs=None, format=None):
        attrs = {"type": "date", **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class SplitDateTimeWidgetCustom(forms.SplitDateTimeWidget):
    """
    Date/time widget with custom styling and date-picker.
    Must be used with `django.forms.SplitDateTimeField`.
    """

    template_name = "common/split_datetime_custom.html"

    def __init__(self, attrs=None):
        widgets = [DateDateInput, forms.TimeInput]
        forms.MultiWidget.__init__(self, widgets, attrs)
