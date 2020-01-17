from django import forms
from quotes.models import Quote
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class QuoteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "quote_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-6 form-field"
    helper.add_input(Submit("submit", "Legg inn"))
    class Meta:
        model = Quote
        fields = ["title", "text", "owner"]
        widgets = {
            "text": forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }
        labels = {
            "owner": "Eier",
            "text": "Tekst",
            "title": "Tittel"
        }