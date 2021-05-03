"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.forms import formset_factory, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, HTML
from crispy_forms.bootstrap import Alert
from sheetmusic.models import Score, Pdf, Part


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

class EditPartForm(forms.ModelForm):
    """ Form for editing a score """
    helper = FormHelper()
    helper.form_id = "sheetmusic_edit_part_form"
    helper.form_method = "post"
    helper.form_action = "login"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-12 form-label"
    helper.field_class = "col-lg-6 form-field"
    # helper.add_input(Submit("submit", "Lagre"))
    helper.layout = Layout(
        Field("name"),
        HTML("<a href='./'> link </a>"),
        Field("pages"),
    )
    pages = forms.CharField(
        label="Sider",
        max_length=0xff,
        required=True,
    )

    class Meta:
        model = Part
        fields = ["name", "pages"]

class EditScoreForm_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout(
            Field("name"),
            Alert(content="Hmmmm, nå da?"),
            HTML("<a href='./'> link </a>"),
            Field("pages"),
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = 'bootstrap/table_inline_formset.html'

# EditScoreForm = modelformset_factory(Part, fields=["name", "pages"])
EditScoreForm = formset_factory(EditPartForm)

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
