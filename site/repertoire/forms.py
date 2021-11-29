"""Forms for the 'sheetmusic'-app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from . import models


class RepertoireCreateForm(forms.ModelForm):
    """Form for creating a new repertoire"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = models.Repertoire
        fields = ["title"]
        labels = {"title": "Tittel"}


class RepertoireUpdateForm(forms.ModelForm):
    """Form for editing a repertoire"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.form_tag = False

    class Meta:
        model = models.Repertoire
        fields = ["title"]
        labels = {"title": "Tittel"}


class RepertoireEntryUpdateForm(forms.ModelForm):
    """Form for creating a repertoire entry"""

    class Meta:
        model = models.RepertoireEntry
        fields = ["score"]
        labels = {
            "score": "Note",
        }

    def save(self, commit: bool = ...) -> models.RepertoireEntry:
        print("skal save RepertoireEntryUpdateForm")
        return super().save(commit=commit)


class RepertoireEntryUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.form_tag = False
        self.template = "common/table_inline_formset_shade_delete.html"


RepertoireEntryUpdateFormset = forms.inlineformset_factory(
    models.Repertoire,
    models.RepertoireEntry,
    form=RepertoireEntryUpdateForm,
    extra=1,
)


class RepertoireEntryCreateForm(forms.ModelForm):
    """Form for creating a repertoire entry"""

    # helper = FormHelper()
    # helper.form_method = "post"
    # helper.label_class = "form-label"
    # helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = models.RepertoireEntry
        fields = ["score"]
        labels = {"score": "Note"}
