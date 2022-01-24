from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    Form,
    ModelChoiceField,
    ModelForm,
    formset_factory,
    inlineformset_factory,
)

from sheetmusic.models import Part, Score

from .models import Repertoire, RepertoireEntry


class RepertoireForm(ModelForm):
    """Form for creating and editing repertoires."""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Repertoire
        fields = ["name"]


class RepertoireEntryForm(ModelForm):
    """Form for creating and editing a repertoire entry."""

    class Meta:
        model = RepertoireEntry
        fields = ["score"]


class RepertoireEntryFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.form_tag = False
        self.template = "common/table_inline_formset_shade_delete.html"


RepertoireEntryFormset = inlineformset_factory(
    Repertoire,
    RepertoireEntry,
    form=RepertoireEntryForm,
    extra=20,
)

RepertoireEntryFormset.helper = RepertoireEntryFormsetHelper()


class RepertoirePdfForm(Form):
    """
    Form for an entry (pair of score and part) for generating a repertoire PDF.
    """

    score = ModelChoiceField(queryset=Score.objects.all(), label="Note", disabled=True)
    part = ModelChoiceField(queryset=Part.objects.all(), label="Stemme")

    # class Meta:
    #     widgets = {
    #         "score": HiddenInput()
    #     }


class RepertoirePdfFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input(Submit("submit", "Generer PDF"))
        self.template = "common/table_inline_formset_shade_delete.html"


RepertoirePdfFormset = formset_factory(form=RepertoirePdfForm, extra=0)


RepertoirePdfFormset.helper = RepertoirePdfFormsetHelper()
