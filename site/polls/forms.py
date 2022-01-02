from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import Choice, Poll, Vote


class PollCreateForm(forms.ModelForm):
    """Form for creating a poll."""

    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Poll
        fields = ["question", "public", "type"]


class PollUpdateForm(forms.ModelForm):
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


class SingleVoteForm(forms.Form):
    """Form for voting on a single-choice poll."""

    choices = forms.ModelChoiceField(None, label="Val", widget=forms.RadioSelect)

    helper = FormHelper()
    helper.add_input(Submit("submit", "Stem"))

    def __init__(self, poll=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.user = user
        self.fields["choices"].queryset = Choice.objects.filter(poll=self.poll)

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

    choices = forms.ModelMultipleChoiceField(
        None, label="Val", widget=forms.CheckboxSelectMultiple
    )

    def save(self):
        choices = self.cleaned_data["choices"]
        Vote.objects.bulk_create(
            [Vote(choice=choice, user=self.user) for choice in choices]
        )
