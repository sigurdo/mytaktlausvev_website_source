from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    """Form for creating comments."""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lag/endre kommentar"))
    helper.form_action = reverse_lazy("comment_create")

    class Meta:
        model = Comment
        fields = ["comment", "content_type", "object_pk"]
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_pk": forms.HiddenInput(),
        }


class CommentUpdateForm(forms.ModelForm):
    """Form for updating comments."""

    helper = FormHelper()
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Rediger kommentar"))

    class Meta:
        model = Comment
        fields = ["comment"]