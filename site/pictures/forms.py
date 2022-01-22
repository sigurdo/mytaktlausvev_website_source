from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ClearableFileInput, DateInput, ModelForm
from django.forms.models import inlineformset_factory

from common.mixins import CleanAllFilesMixin

from .models import Gallery, Image


class GalleryForm(ModelForm):
    """Form for creating and editing galleries."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lag/rediger galleri"))

    class Meta:
        model = Gallery
        fields = ["title", "date", "date_to", "content"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
            "date_to": DateInput(attrs={"type": "date"}),
        }


class ImageCreateForm(CleanAllFilesMixin, ModelForm):
    """Form for creating images."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Last opp bilete"))

    def __init__(self, gallery=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gallery = gallery
        self.user = user

    def save(self, commit=True):
        """
        Save all uploaded images using `bulk_create`.
        Ignores `commit` parameter.
        """
        Image.objects.bulk_create(
            [
                Image(gallery=self.gallery, image=image, uploaded_by=self.user)
                for image in self.files.getlist("image")
            ]
        )

    class Meta:
        model = Image
        fields = ["image"]
        widgets = {
            "image": ClearableFileInput(attrs={"multiple": True}),
        }


class ImageUpdateForm(ModelForm):
    """Form for updating an image."""

    class Meta:
        model = Image
        fields = ["image", "description"]


class ImageFormsetHelper(FormHelper):
    template = "pictures/image_formset.html"


ImageFormSet = inlineformset_factory(
    Gallery,
    Image,
    form=ImageUpdateForm,
    can_delete=False,
    extra=0,
)
ImageFormSet.helper = ImageFormsetHelper()
