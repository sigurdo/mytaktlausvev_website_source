from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, inlineformset_factory

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
    extra=5,
)

RepertoireEntryFormset.helper = RepertoireEntryFormsetHelper()
