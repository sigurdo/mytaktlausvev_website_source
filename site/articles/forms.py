from tkinter import Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from common.forms.widgets import AutocompleteSelect

from .models import Article


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger artikkel"))

    class Meta:
        model = Article
        fields = ["title", "content", "parent", "public", "comments_allowed"]
        labels = {"parent": "Underartikkel av"}
        widgets = {"parent": AutocompleteSelect}
