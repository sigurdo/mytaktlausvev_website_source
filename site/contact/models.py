from django.db.models import CharField, EmailField, FloatField, Model


class ContactCategory(Model):
    """
    Model for a category on the contact form.

    `name` is the name of the category.
    Indicates what the email is about, and who receives it.

    `email` is the email the form is sent to.
    """

    name = CharField("namn", max_length=255, unique=True)
    email = EmailField("e-post")
    order = FloatField(
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
