from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from .models import Topic


class TopicCreateForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Opprett emne"))

    class Meta:
        model = Topic
        fields = ["title"]
