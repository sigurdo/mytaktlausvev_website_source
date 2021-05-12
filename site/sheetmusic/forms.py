"""Forms for the 'sheetmusic'-app"""
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, modelformset_factory, widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, HTML
from crispy_forms.bootstrap import Alert
from .models import Score, Pdf, Part
from .utils import convertPagesToInputFormat, convertInputFormatToPages


class ScoreCreateForm(forms.ModelForm):
    """Form for uploading a new score"""
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
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
    """ Form for editing a part """
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"

    class Meta:
        model = Part
        fields=["name", "fromPage", "toPage", "pdf"]
        labels={ "name": "Navn", "fromPage": "Første side", "toPage": "Siste side" }
        widgets={ "fromPage": forms.NumberInput(attrs={ "size": 1 }), "toPage": forms.NumberInput(attrs={ "size": 1 }), "pdf": forms.HiddenInput() }

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

EditPartFormSet = modelformset_factory(Part,
    # fields=["name", "fromPage", "toPage"],
    # labels={ "name": "Navn", "fromPage": "Første side", "toPage": "Siste side" },
    # widgets={ "fromPage": forms.NumberInput(attrs={ "size": 1 }), "toPage": forms.NumberInput(attrs={ "size": 1 }) },
    form=EditPartForm,
    extra=0)

# class EditPdfForm(forms.ModelForm):
#     """ Form for editing a part """
#     helper = FormHelper()
#     helper.form_method = "post"
#     helper.label_class = "form-label"

#     class Meta:
#         model = Pdf
#         fields=["name", "fromPage", "toPage", "pdf"]
#         labels={ "name": "Navn", "fromPage": "Første side", "toPage": "Siste side" }
#         widgets={ "fromPage": forms.NumberInput(attrs={ "size": 1 }), "toPage": forms.NumberInput(attrs={ "size": 1 }), "pdf": forms.HiddenInput() }

class EditScoreForm(forms.ModelForm):
    """ Form for editing a score """
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Lagre"))

    class Meta:
        model = Score
        fields = ["title"]
        labels = {
            "title": "Tittel"
        }

class UploadPdfForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"
    helper.label_class = "form-label"
    helper.add_input(Submit("submit", "Last opp"))

    class Meta:
        model = Pdf
        fields = ["file"]
        labels = {
            "file": "Fil"
        }
