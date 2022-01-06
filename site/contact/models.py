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
    order = models.IntegerField(
        "rekkjefølgje",
        default=0,
        help_text="Definerer rekkjefølgja til kategoriar. Kategoriar med lik rekkjefølgje blir sortert etter namn.",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "kontaktkategori"
        verbose_name_plural = "kontaktkategoriar"
