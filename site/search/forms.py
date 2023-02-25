from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import CharField, Form, TextInput
from django.urls import reverse_lazy


class SearchForm(Form):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Søk"))
    helper.form_method = "get"
    helper.form_action = reverse_lazy("search:Search")
    helper.attrs = {
        "data-hx-get": reverse_lazy("search:Search"),
        "data-hx-target": "#search-results",
        "data-hx-swap": "innerHTML",
        "data-hx-push-url": "true",
        "data-hx-indicator": ".htmx-indicator",
    }

    query = CharField(
        label="Søk",
        max_length=255,
        widget=TextInput(
            {
                "type": "search",
                "data-hx-trigger": "keyup changed delay:500ms, search",
                "data-hx-get": reverse_lazy("search:Search"),
                "autofocus": True,
            }
        ),
    )
