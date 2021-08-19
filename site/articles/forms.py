from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Article


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger artikkel"))

    class Meta:
        model = Article
        fields = ["title", "description", "public", "comments_allowed"]
