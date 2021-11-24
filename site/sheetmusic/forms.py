"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.forms import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Score, Pdf, Part


class ScoreCreateForm(forms.ModelForm):
    """Form for uploading a new score"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = ["title"]
        labels = {"title": "Tittel"}


class EditPartForm(forms.ModelForm):
    """Form for editing a part"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"

    class Meta:
        model = Part
        fields = ["name", "from_page", "to_page", "pdf"]
        labels = {"name": "Navn", "from_page": "Første side", "to_page": "Siste side"}
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


class EditScoreForm(forms.ModelForm):
    """Form for editing a score"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = ["title"]
        labels = {"title": "Tittel"}


class UploadPdfForm(forms.Form):
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Last opp"))
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), label="Filer"
    )


class EditPdfForm(forms.ModelForm):
    """Form for editing a pdf"""

    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"

    class Meta:
        model = Pdf
        fields = ["file"]
        labels = {"file": "Fil"}
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
