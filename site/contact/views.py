import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.generic import FormView

from contact.forms import ContactForm

logger = logging.getLogger(__name__)


class ContactView(FormView):
    template_name = "contact/contact.html"
    template_success_name = "contact/success.html"
    form_class = ContactForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update(
                {"name": self.request.user.username, "email": self.request.user.email}
            )
        return initial

    def _get_email_subject(self, form):
        """
        Returns the email subject in the form
        "[<category_name>] <subject>".
        """
        category_name = form.cleaned_data["category"].name
        subject = form.cleaned_data["subject"]
        return f"[{category_name}] {subject}"

    def _get_email_body(self, form):
        """Returns the email body with an intro message."""
        intro = f"{form.cleaned_data['name']} ({form.cleaned_data['email']}) sende ei melding gjennom kontaktskjemaet på nettsida."
        return f"{intro}\n\n{form.cleaned_data['message']}"

    def _get_reply_to_mail(self, form):
        """Returns the reply to mail, including the sender's name."""
        return f'"{form.cleaned_data["name"]}" <{form.cleaned_data["email"]}>'

    def _is_spam(self, form) -> bool:
        """
        Returns `True` if the form is spam, otherwise `False`.
        A form is considered to be spam if the hidden field `content`
        has been modified.
        """
        return bool(form.cleaned_data["content"])

    def form_valid(self, form):
        if self._is_spam(form):
            logging.warn("Spam detected in contact form. Rejecting message.")
            return render(self.request, self.template_success_name)

        try:
            EmailMessage(
                self._get_email_subject(form),
                self._get_email_body(form),
                settings.EMAIL_HOST_USER,
                [form.cleaned_data["category"].email],
                headers={
                    "Reply-To": self._get_reply_to_mail(form),
                },
            ).send(fail_silently=False)
        except SMTPException:
            form.add_error(None, "Sendinga av meldinga mislykkast. Prøv igjen seinare.")
            return self.form_invalid(form)

        return render(self.request, self.template_success_name)
