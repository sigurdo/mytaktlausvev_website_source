from django.forms import ModelForm, inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Repertoire, RepertoireEntry


class RepertoireCreateForm(ModelForm):
    """Form for creating a new repertoire"""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Repertoire
        fields = ["name"]


class RepertoireUpdateForm(ModelForm):
    """Form for editing a repertoire"""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Repertoire
        fields = ["name"]


class RepertoireEntryUpdateForm(ModelForm):
    """Form for creating a repertoire entry"""

    class Meta:
        model = RepertoireEntry
        fields = ["score"]
        labels = {
            "score": "Note",
        }


class RepertoireEntryUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.form_tag = False
        self.template = "common/table_inline_formset_shade_delete.html"


RepertoireEntryUpdateFormset = inlineformset_factory(
    Repertoire,
    RepertoireEntry,
    form=RepertoireEntryUpdateForm,
    extra=5,
)

RepertoireEntryUpdateFormset.helper = RepertoireEntryUpdateFormsetHelper()
