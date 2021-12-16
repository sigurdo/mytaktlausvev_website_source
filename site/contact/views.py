from smtplib import SMTPException
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views.generic import FormView
from django.shortcuts import render
from contact.forms import ContactForm


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
        ...
        """
        category_name = form.cleaned_data["category"].name
        subject = form.cleaned_data["subject"]
        return f"[{category_name}] {subject}"

    def _get_email_body(self, form):
        """Returns the email body with an intro message."""
        intro = f"{form.cleaned_data['name']} ({form.cleaned_data['email']}) sende ei melding gjennom kontaktskjemaet på nettsida."
        return f"{intro}\n\n{form.cleaned_data['message']}"

    def _get_from_mail(self, form):
        """Returns the from mail, including the sender's name."""
        return f'"{form.cleaned_data["name"]}" <{form.cleaned_data["email"]}>'

    def _get_to_mails(self, form):
        """
        Returns the emails to send the message to.
        Always includes the category's email.
        Includes the sender's email if `send_to_self` is true.
        """
        mail_self = form.cleaned_data["email"]
        mail_category = form.cleaned_data["category"].email

        if form.cleaned_data["send_to_self"]:
            return [mail_category, mail_self]
        return [mail_category]

    def form_valid(self, form):
        try:
            EmailMessage(
                self._get_email_subject(form),
                self._get_email_body(form),
                settings.EMAIL_HOST_USER,
                self._get_to_mails(form),
                headers={
                    "From": self._get_from_mail(form),
                    "Sender": settings.EMAIL_HOST_USER,
                },
            ).send(fail_silently=False)
        except SMTPException:
            form.add_error(None, "Sendinga av meldinga mislykkast. Prøv igjen seinare.")
            return self.form_invalid(form)

        return render(
            self.request,
            self.template_success_name,
            {"copy_sent_to_self": form.cleaned_data["send_to_self"]},
        )
