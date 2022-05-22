from io import BytesIO

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    Form,
    IntegerField,
    ModelChoiceField,
    ModelForm,
    Select,
    formset_factory,
    inlineformset_factory,
)
from django.urls import reverse
from PyPDF2 import PdfFileReader, PdfFileWriter

from common.forms import DynamicFormsetButton
from sheetmusic.models import Part, Score

from .models import Repertoire, RepertoireEntry


class RepertoireForm(ModelForm):
    """Form for creating and editing repertoires."""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Repertoire
        fields = ["name", "order"]


class RepertoireEntryForm(ModelForm):
    """Form for creating and editing a repertoire entry."""

    class Meta:
        model = RepertoireEntry
        fields = ["score"]


class RepertoireEntryFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.add_input(DynamicFormsetButton("Legg til enda en oppføring"))
        self.add_input(Submit("submit", "Lagre"))
        self.form_tag = False
        self.template = "common/table_inline_formset_shade_delete.html"


RepertoireEntryFormset = inlineformset_factory(
    Repertoire,
    RepertoireEntry,
    form=RepertoireEntryForm,
    extra=1,
)

RepertoireEntryFormset.helper = RepertoireEntryFormsetHelper()


class PartChoiceWidget(Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        # This allows using strings labels as usual
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop("label")
        else:
            opt_attrs = {}
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        for key, val in opt_attrs.items():
            option_dict["attrs"][key] = val
        return option_dict


class PartChoiceField(ModelChoiceField):
    """
    ChoiceField that puts data-pdf-url on <option>s.
    Waterfall-boiled from https://stackoverflow.com/a/63293300/9395922
    """

    widget = PartChoiceWidget

    def label_from_instance(self, part):
        return {
            # the usual label:
            "label": super().label_from_instance(part),
            # the new data attribute:
            "data-pdf-url": reverse(
                "sheetmusic:PartPdf", args=[part.pdf.score.slug, part.slug]
            ),
        }


class RepertoirePdfForm(Form):
    """
    Form for an entry (pair of score and part) for generating a repertoire PDF.
    """

    score = ModelChoiceField(queryset=Score.objects.all(), label="Note", disabled=True)
    part = PartChoiceField(queryset=Part.objects.none(), label="Stemme", required=False)
    amount = IntegerField(min_value=0, max_value=63, label="Antal", initial=1)


class RepertoirePdfFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input(Submit("submit", "Generer PDF"))
        self.template = "common/table_inline_formset_shade_delete.html"


def RepertoirePdfFormset_save(self):
    pdf_writer = PdfFileWriter()
    for form in self:
        part = form.cleaned_data["part"]
        if part is None:
            continue
        for _ in range(form.cleaned_data["amount"]):
            pdf_writer.appendPagesFromReader(PdfFileReader(part.pdf_file()))
    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return output_stream


RepertoirePdfFormset = formset_factory(form=RepertoirePdfForm, extra=0)
RepertoirePdfFormset.save = RepertoirePdfFormset_save


RepertoirePdfFormset.helper = RepertoirePdfFormsetHelper()
