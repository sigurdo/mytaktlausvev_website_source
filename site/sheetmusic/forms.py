"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.forms import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Score, Pdf, Part


class ScoreForm(forms.ModelForm):
    """Form for creating or changing a score"""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = ["title"]


class EditPartForm(forms.ModelForm):
    """Form for editing a part"""

    helper = FormHelper()

    class Meta:
        model = Part
        fields = ["name", "from_page", "to_page", "pdf"]
        widgets = {
            "from_page": forms.NumberInput(attrs={"size": 1}),
            "to_page": forms.NumberInput(attrs={"size": 1}),
            "pdf": forms.Select(),
        }


class EditPartFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


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
        self.form_method = "post"
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = "common/table_inline_formset_shade_delete.html"


EditPdfFormset.helper = EditPdfFormsetHelper()
