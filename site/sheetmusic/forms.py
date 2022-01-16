"""Forms for the 'sheetmusic'-app"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, FileField, modelformset_factory

from .models import Part, Pdf, Score, pdf_file_validators


class ScoreForm(forms.ModelForm):
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


class PartsUpdateForm(forms.ModelForm):
    """Form for editing a part for a given pdf"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["from_page", "name", "to_page"]
        widgets = {
            "name": forms.TextInput(attrs={"size": 30}),
            "from_page": forms.NumberInput(attrs={"size": 4}),
            "to_page": forms.NumberInput(attrs={"size": 4}),
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


class PartsUpdateAllForm(forms.ModelForm):
    """Form for editing a part"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["name", "from_page", "to_page", "pdf"]
        widgets = {
            "name": forms.TextInput(attrs={"size": 50}),
            "from_page": forms.NumberInput(attrs={"size": 4}),
            "to_page": forms.NumberInput(attrs={"size": 4}),
        }


PartsUpdateAllFormset = modelformset_factory(
    Part,
    form=PartsUpdateAllForm,
    can_delete=True,
    extra=20,
)


PartsUpdateAllFormset.helper = PartsUpdateFormsetHelper()


class UploadPdfForm(forms.Form):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Last opp"))
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
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

    def _clean_fields(self):
        super()._clean_fields()
        # For some reason, django only calls field.clean() on the last file, so
        # we have to call field.clean() on all the others manually
        for name, field in self.fields.items():
            if isinstance(field, FileField):
                for file in self.files.getlist("files")[:-1]:
                    try:
                        field.clean(file)
                    except ValidationError as exception:
                        self.add_error(name, exception)


class EditPdfForm(forms.ModelForm):
    """Form for editing a pdf"""

    helper = FormHelper()

    class Meta:
        model = Pdf
        fields = ["file"]
        widgets = {"file": forms.ClearableFileInput(attrs={"disabled": True})}


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
