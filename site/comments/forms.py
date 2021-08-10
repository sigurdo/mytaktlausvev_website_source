from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments."""

    helper = FormHelper()
    helper.form_action = reverse_lazy("comment_create")
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lag/endre kommentar"))

    class Meta:
        model = Comment
        fields = ["comment", "content_type", "object_pk"]
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_pk": forms.HiddenInput(),
        }
