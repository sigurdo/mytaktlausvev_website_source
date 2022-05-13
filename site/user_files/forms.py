from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from .models import File


class FileForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre fil"))

    class Meta:
        model = File
        fields = ["name", "file", "public"]
