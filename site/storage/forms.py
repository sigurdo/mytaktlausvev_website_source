from crispy_forms.helper import FormHelper
from django.forms import ModelForm, modelformset_factory

from accounts.models import UserCustom


class StorageAccessUpdateForm(ModelForm):
    class Meta:
        model = UserCustom
        fields = [
            "has_storage_access",
        ]


class StorageAccessUpdateFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "storage/storage_access_formset.html"


StorageAccessUpdateFormset = modelformset_factory(
    UserCustom, form=StorageAccessUpdateForm, extra=0
)


StorageAccessUpdateFormset.helper = StorageAccessUpdateFormsetHelper()
