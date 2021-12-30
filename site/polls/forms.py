from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, widgets
from django.forms.models import inlineformset_factory

from .models import Choice, Poll, Vote


class PollForm(forms.ModelForm):
    """Form for creating or editing a poll."""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Poll
        fields = ["question", "public", "type"]


class ChoiceForm(forms.ModelForm):
    """Form for creating or editing a choice in a poll."""

    helper = FormHelper()

    class Meta:
        model = Choice
        fields = ["text"]


class ChoiceFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "common/table_inline_formset_shade_delete.html"
        self.form_tag = False
        self.add_input(Submit("submit", "Lagre avstemming"))


ChoiceFormset = inlineformset_factory(
    Poll,
    Choice,
    form=ChoiceForm,
    can_delete=True,
    extra=10,
)


ChoiceFormset.helper = ChoiceFormsetHelper()


class VoteCreateForm(forms.ModelForm):
    """Form for voting on a poll."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Stem"))

    def __init__(self, poll=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.fields["choice"].queryset = Choice.objects.filter(poll=self.poll)

    def clean(self):
        super().clean()
        if self.poll.has_voted(self.instance.user):
            raise ValidationError("Du har allereie stemt.")

    class Meta:
        model = Vote
        fields = ["choice"]
        widgets = {"choice": forms.widgets.RadioSelect}
