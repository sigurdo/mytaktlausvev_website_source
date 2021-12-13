"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.forms import modelformset_factory, ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Score, Pdf, Part


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
            "description",
            "sound_file",
            "sound_link",
        ]


class EditPartForm(forms.ModelForm):
    """Form for editing a part"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["name", "from_page", "to_page", "pdf"]
        widgets = {
            "from_page": forms.NumberInput(attrs={"size": 3}),
            "to_page": forms.NumberInput(attrs={"size": 3}),
        }


class EditPartFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_required_fields = True
        self.template = "common/table_inline_formset_shade_delete.html"
        self.add_input(Submit("submit", "Lagre"))


EditPartFormSet = modelformset_factory(
    Part,
    form=EditPartForm,
    can_delete=True,
    extra=1,
)


EditPartFormSet.helper = EditPartFormSetHelper()


class UploadPdfForm(forms.Form):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Last opp"))
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), label="Filer"
    )
    part_prediction = ChoiceField(choices=[("sheatless", "sheatless",), ("filename", "filnavn",), ("none", "ingen",)], label="Gjett stemmer ved hjelp av")


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
