from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.models import inlineformset_factory
from .models import Gallery, Image


class GalleryForm(forms.ModelForm):
    """Form for creating and editing galleries."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger galleri"))

    class Meta:
        model = Gallery
        fields = ["title", "date", "date_to", "content"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "date_to": forms.DateInput(attrs={"type": "date"}),
        }


class ImageForm(forms.ModelForm):
    """Form for images."""

    class Meta:
        model = Image
        fields = ["image"]


class ImageFormsetHelper(FormHelper):
    template = "pictures/image_formset.html"


ImageFormSet = inlineformset_factory(
    Gallery,
    Image,
    form=ImageForm,
    can_delete=False,
    extra=0,
)
ImageFormSet.helper = ImageFormsetHelper()
