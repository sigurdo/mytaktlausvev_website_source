"""Forms for the 'sheetmusic'-app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from sheetmusic.models import Score, Pdf


class CreateScoreForm(forms.ModelForm):
    """Form for uploading a new score"""
    helper = FormHelper()
    helper.form_id = "sheetmusic_upload_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-6 form-field"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = ["title"]
        labels = {
            "title": "Tittel"
        }

class UploadPdfForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "sheetmusic_upload_pdf_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-6 form-field"
    helper.add_input(Submit("submit", "Last opp"))

    class Meta:
        model = Pdf
        fields = ["file"]
        labels = {
            "file": "Fil"
        }
