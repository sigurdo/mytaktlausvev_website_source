from django import forms
from quotes.models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["owner", "text", "title"]
        widgets = {
            "text": forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }
        labels = {
            "owner": "Eier",
            "text": "Tekst",
            "title": "Tittel"
        }