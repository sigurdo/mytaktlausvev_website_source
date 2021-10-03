from django.core.mail import send_mail
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
        intro = f"{form.cleaned_data['name']} sende ei melding gjennom kontaktskjemaet på nettsida."
        return f"{intro}\n\n{form.cleaned_data['message']}"

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
        send_mail(
            self._get_email_subject(form),
            self._get_email_body(form),
            form.cleaned_data["email"],
            self._get_to_mails(form),
            fail_silently=False,
        )
        return render(
            self.request,
            self.template_success_name,
            {"copy_sent_to_self": form.cleaned_data["send_to_self"]},
        )
