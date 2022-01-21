"""Forms for the 'sheetmusic'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    ChoiceField,
    ClearableFileInput,
    FileField,
    Form,
    ModelForm,
    NumberInput,
    TextInput,
    modelformset_factory,
)

from common.mixins import CleanAllFilesMixin

from .models import Part, Pdf, Score, pdf_file_validators


class ScoreForm(ModelForm):
    """Form for creating or changing a score"""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = [
            "title",
            "arrangement",
            "originally_from",
            "content",
            "sound_file",
            "sound_link",
        ]


class PartsUpdateForm(ModelForm):
    """Form for editing a part for a given pdf"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["from_page", "name", "to_page"]
        widgets = {
            "name": TextInput(attrs={"size": 30}),
            "from_page": NumberInput(attrs={"size": 4}),
            "to_page": NumberInput(attrs={"size": 4}),
        }


class PartsUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.template = "common/table_inline_formset_shade_delete.html"
        self.add_input(Submit("submit", "Lagre"))


PartsUpdateFormset = modelformset_factory(
    Part,
    form=PartsUpdateForm,
    can_delete=True,
    extra=20,
)


PartsUpdateFormset.helper = PartsUpdateFormsetHelper()


class PartsUpdateAllForm(ModelForm):
    """Form for editing a part"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["name", "from_page", "to_page", "pdf"]
        widgets = {
            "name": TextInput(attrs={"size": 50}),
            "from_page": NumberInput(attrs={"size": 4}),
            "to_page": NumberInput(attrs={"size": 4}),
        }


PartsUpdateAllFormset = modelformset_factory(
    Part,
    form=PartsUpdateAllForm,
    can_delete=True,
    extra=20,
)


PartsUpdateAllFormset.helper = PartsUpdateFormsetHelper()


class UploadPdfForm(CleanAllFilesMixin, Form):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Last opp"))
    files = FileField(
        widget=ClearableFileInput(attrs={"multiple": True}),
        label="Filer",
        validators=pdf_file_validators,
    )
    part_prediction = ChoiceField(
        choices=[
            (
                "sheatless",
                "Sheatless",
            ),
            (
                "filename",
                "Filnavn",
            ),
            (
                "none",
                "Ingen",
            ),
        ],
        label="Gjett stemmer ved hjelp av",
    )


class EditPdfForm(ModelForm):
    """Form for editing a pdf"""

    helper = FormHelper()

    class Meta:
        model = Pdf
        fields = ["file"]
        widgets = {"file": ClearableFileInput(attrs={"disabled": True})}


EditPdfFormset = modelformset_factory(
    Pdf,
    form=EditPdfForm,
    can_delete=True,
    extra=0,
)


class EditPdfFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.template = "common/table_inline_formset_shade_delete.html"
        self.add_input(Submit("submit", "Lagre"))


EditPdfFormset.helper = EditPdfFormsetHelper()
