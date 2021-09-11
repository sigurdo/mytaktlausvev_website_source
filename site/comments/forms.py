from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    """Form for creating comments."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Legg ut kommentar"))
    helper.form_action = "comment_create"

    class Meta:
        model = Comment
        fields = ["comment", "content_type", "object_pk"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
            "content_type": forms.HiddenInput(),
            "object_pk": forms.HiddenInput(),
        }


class CommentUpdateForm(forms.ModelForm):
    """Form for updating comments."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Rediger kommentar"))

    class Meta:
        model = Comment
        fields = ["comment"]
