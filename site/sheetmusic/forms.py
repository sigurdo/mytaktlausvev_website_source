"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, modelformset_factory, widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, HTML
from crispy_forms.bootstrap import Alert
from sheetmusic.models import Score, Pdf, Part
from sheetmusic.utils import convertPagesToInputFormat, convertInputFormatToPages


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

def validatePagesField(value):
    # print("validatePagesField")
    try:
        fromPage, toPage = convertInputFormatToPages(value)
        if not fromPage <= toPage:
            raise Exception()
    except:
        raise ValidationError("Pages is not valid: %(value)s", params={ "value": value })

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
    # helper.layout = Layout(
    #     Field("name"),
    #     HTML("<a href='./'> link </a>"),
    #     Field("pages"),
    # )
    pages = forms.CharField(
        label="Sider",
        max_length=0xff,
        required=True,
        validators=[validatePagesField],
    )
    # pk = forms.HiddenInput()

    class Meta:
        model = Part
        widgets = {
            # "name": forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            "id": forms.HiddenInput()
        }
        fields = ["name", "pages", "id"]

# class EditPartForm(forms.Form):
#     name = forms.CharField(
#         label="Navn",
#         max_length=0xff,
#         required=True,
#     )
#     pages = forms.CharField(
#         label="Sider",
#         max_length=0xff,
#         required=True,
#         validators=[validatePagesField],
#     )
#     pk = forms.CharField()

# EditScoreForm = modelformset_factory(Part, fields=["name", "pages"])
# EditScoreForm = formset_factory(EditPartForm)

class EditPartFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.add_input(Submit("submit", "Lagre"))
        self.template = 'sheetmusic/table_inline_formset_for_edit_score_form.html'

EditPartFormSet = modelformset_factory(Part, fields=["name", "fromPage", "toPage"], extra=0)

class EditScoreForm(forms.ModelForm):
    """ Form for editing a score """
    helper = FormHelper()
    helper.form_id = "sheetmusic_edit_part_form"
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
