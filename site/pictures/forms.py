from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import (
    ClearableFileInput,
    DateInput,
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.models import inlineformset_factory

from common.forms.mixins import CleanAllFilesMixin
from common.forms.widgets import AutocompleteSelectMultiple
from events.models import Event

from .models import Gallery, Image


class GalleryForm(ModelForm):
    """Form for creating and editing galleries."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Lagre galleri"))

    events = ModelMultipleChoiceField(
        queryset=Event.objects.order_by("-start_time"),
        required=False,
        widget=AutocompleteSelectMultiple,
        label="Hendingar",
    )

    class Meta:
        model = Gallery
        fields = ["title", "date", "date_to", "content", "events"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
            "date_to": DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.initial["events"] = self.instance.events.all()

    def save(self):
        gallery = super().save()
        gallery.events.set(self.cleaned_data["events"])
        return gallery


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
    extra=0,
)
ImageFormSet.helper = ImageFormsetHelper()
