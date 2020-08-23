from django import forms
from julekalender.models import Julekalender
from julekalender.models import Window


class NewJulekalenderForm(forms.ModelForm):
    """Form for creating a new julekalender"""

    class Meta:
        model = Julekalender
        fields = ["year"]
        labels = {"year": "År"}


class NewWindowForm(forms.ModelForm):
    """Form for posting a new window"""

    title = forms.CharField(label="Tittel", max_length=255)
    post = forms.CharField(label="Post", widget=forms.Textarea)
    index = forms.IntegerField(label="Lukenummer", min_value=1, max_value=24)

    class Meta:
        model = Window
        fields = ["title", "post", "index"]
        labels = {"title": "Tittel"}
