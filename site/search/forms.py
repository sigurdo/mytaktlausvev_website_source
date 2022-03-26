from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import CharField, Form


class SearchForm(Form):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Søk"))
    helper.form_action = "search:Search"
    helper.form_method = "get"

    q = CharField(label="Søk", max_length=255)
