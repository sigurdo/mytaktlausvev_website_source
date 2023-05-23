"""Forms for the 'sheetmusic'-app"""
import threading

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    ChoiceField,
    ClearableFileInput,
    FileField,
    Form,
    ModelForm,
    NumberInput,
    ValidationError,
    modelformset_factory,
)

from common.forms.layouts import DynamicFormsetButton
from common.forms.mixins import CleanAllFilesMixin

from .models import EditFile, Part, Pdf, Score, pdf_file_validators


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
            "transcribed_by",
            "content",
            "sound_file",
            "sound_link",
        ]
        widgets = {
            "sound_file": ClearableFileInput(attrs={"accept": "audio/*"}),
        }


class PartsUpdateForm(ModelForm):
    """Form for editing a part for a given pdf"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["from_page", "instrument_type", "part_number", "note", "to_page"]
        labels = {"part_number": "Stemme-nummer"}
        widgets = {
            "part_number": NumberInput(attrs={"size": 4}),
            "from_page": NumberInput(attrs={"size": 4}),
            "to_page": NumberInput(attrs={"size": 4}),
        }


class PartsUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.template = "common/forms/table_inline_formset_shade_delete.html"
        self.add_input(DynamicFormsetButton("Legg til endå ein stemme"))
        self.add_input(Submit("submit", "Lagre"))


PartsUpdateFormset = modelformset_factory(
    Part,
    form=PartsUpdateForm,
    can_delete=True,
    extra=1,
)


PartsUpdateFormset.helper = PartsUpdateFormsetHelper()


class PartsUpdateAllForm(ModelForm):
    """Form for editing a part"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = [
            "instrument_type",
            "part_number",
            "note",
            "from_page",
            "to_page",
            "pdf",
        ]
        widgets = {
            "from_page": NumberInput(attrs={"size": 4}),
            "to_page": NumberInput(attrs={"size": 4}),
        }


PartsUpdateAllFormset = modelformset_factory(
    Part,
    form=PartsUpdateAllForm,
    can_delete=True,
    extra=1,
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
                "Filnamn",
            ),
            (
                "none",
                "Ingen",
            ),
        ],
        label="Strategi for å finne stemmer automatisk",
    )

    def save(self, score, plz_wait=False):
        """
        Saves the form

        The sheatless processing is performed in another thread by default so that the
        view can return immediately. If it is desirable to complete the entire processing
        before the function returns this behavior can be overridden by setting plz_wait=True.
        This overrideability is very useful in the test framework.
        """
        for file in self.files.getlist("files"):
            pdf = Pdf.objects.create(
                score=score, file=file, filename_original=file.name
            )
            match self["part_prediction"].value():
                case "sheatless":
                    if plz_wait:
                        pdf.find_parts_with_sheatless()
                    else:
                        processPdfsThread = threading.Thread(
                            target=pdf.find_parts_with_sheatless
                        )
                        processPdfsThread.start()
                case "filename":
                    pdf.find_parts_from_original_filename()
                case "none":
                    pass
                case _:
                    raise ValidationError(
                        "Ulovleg stemmefinningsstrategi: {}".format(
                            self["part_prediction"].value()
                        )
                    )


class EditPdfForm(ModelForm):
    """Form for editing a pdf"""

    helper = FormHelper()

    class Meta:
        model = Pdf
        fields = ["file"]


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
        self.template = "common/forms/table_inline_formset_shade_delete.html"
        self.add_input(Submit("submit", "Lagre"))


EditPdfFormset.helper = EditPdfFormsetHelper()


class UploadEditFilesForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre redigeringsfiler"))

    def save(self, score, commit=True):
        """Saves all submitted files as edit files of `score`. Ignores value of `commit`."""
        for file in self.files.getlist("file"):
            EditFile.objects.create(score=score, file=file, filename_original=file.name)

    class Meta:
        model = EditFile
        fields = ["file"]
        widgets = {"file": ClearableFileInput(attrs={"multiple": True})}
        labels = {"file": "Redigeringsfiler"}


class EditEditFileForm(ModelForm):
    """Form for editing an edit file for a score."""

    helper = FormHelper()

    class Meta:
        model = EditFile
        fields = ["file"]


EditEditFileFormset = modelformset_factory(
    EditFile,
    form=EditEditFileForm,
    can_delete=True,
    extra=0,
)


class EditEditFileFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.template = "common/forms/table_inline_formset_shade_delete.html"
        self.add_input(Submit("submit", "Lagre redigeringsfiler"))


EditEditFileFormset.helper = EditEditFileFormsetHelper()
