from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import (
    CheckboxSelectMultiple,
    Form,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
    NumberInput,
    RadioSelect,
)
from django.forms.models import inlineformset_factory
from django.urls.base import reverse
from django.utils.http import urlencode

from common.forms import DynamicFormsetButton

from .models import Choice, Poll, Vote


class PollCreateForm(ModelForm):
    """Form for creating a poll."""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Poll
        fields = ["question", "public", "type"]


class PollUpdateForm(ModelForm):
    """
    Form for updating a poll.
    Excludes `type` since changing this
    invalidates votes.
    """

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Poll
        fields = ["question", "public"]


class ChoiceForm(ModelForm):
    """Form for creating or editing a choice in a poll."""

    helper = FormHelper()

    class Meta:
        model = Choice
        fields = ["text", "order"]
        help_texts = {"order": ""}
        widgets = {
            "order": NumberInput(attrs={"size": 4}),
        }


class ChoiceFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "common/table_inline_formset_shade_delete.html"
        self.form_tag = False
        self.add_input(DynamicFormsetButton("Legg til val"))
        self.add_input(Submit("submit", "Lagre avstemming"))


ChoiceFormset = inlineformset_factory(
    Poll,
    Choice,
    form=ChoiceForm,
    can_delete=True,
    extra=5,
)


ChoiceFormset.helper = ChoiceFormsetHelper()


class SingleVoteForm(Form):
    """Form for voting on a single-choice poll."""

    choices = ModelChoiceField(None, label="Val", widget=RadioSelect)

    helper = FormHelper()
    helper.add_input(Submit("submit", "Stem"))

    def __init__(self, poll=None, user=None, next=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.user = user
        self.fields["choices"].queryset = Choice.objects.filter(poll=self.poll)

        self.helper.form_action = reverse("polls:VoteCreate", args=[self.poll.slug])
        if next:
            self.helper.form_action += f"?{urlencode({'next': next})}"

    def clean(self):
        """
        Ensure user hasn't voted for the poll yet,
        since this can't be enforced in the database.
        """
        super().clean()
        if self.poll.has_voted(self.user):
            raise ValidationError("Du har allereie stemt.")

    def save(self):
        choice = self.cleaned_data["choices"]
        Vote.objects.create(choice=choice, user=self.user)


class MultiVoteForm(SingleVoteForm):
    """Form for voting on a multiple-choice poll."""

    choices = ModelMultipleChoiceField(None, label="Val", widget=CheckboxSelectMultiple)

    def save(self):
        choices = self.cleaned_data["choices"]
        Vote.objects.bulk_create(
            [Vote(choice=choice, user=self.user) for choice in choices]
        )
