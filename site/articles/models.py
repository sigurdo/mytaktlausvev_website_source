from django.db import models
from django.urls import reverse
from tree_queries.models import TreeNode
from autoslug import AutoSlugField
from common.models import ArticleMixin


class Article(ArticleMixin, TreeNode):
    public = models.BooleanField(
        "offentleg",
        help_text="Om artikkelen er open for ålmente.",
        default=False,
    )
    comments_allowed = models.BooleanField(
        "open for kommentarar",
        default=True,
    )
    slug = AutoSlugField(
        verbose_name="slug",
        populate_from="title",
        unique_with=("title", "parent"),
        editable=True,
    )

    def path(self):
        """Returns a /-separated list of ancestor slugs, including self."""
        slugs = [ancestor.slug for ancestor in self.ancestors(include_self=True)]
        return "/".join(slugs)

    def get_absolute_url(self):
        return reverse("articles:detail", args=[self.path()])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "slug"], name="unique_slug")
        ]
        ordering = ["title"]
