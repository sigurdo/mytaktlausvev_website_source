from django.db import models


class ContactCategory(models.Model):
    """
    Model for a category on the contact form.

    `name` is the name of the category.
    Indicates what the email is about, and who receives it.

    `email` is the email the form is sent to.
    """

    name = models.CharField("namn", max_length=255, unique=True)
    email = models.EmailField("e-post")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "kontaktkategori"
        verbose_name_plural = "kontaktkategoriar"
