from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from tree_queries.models import TreeNode

from common.breadcrumbs.breadcrumbs import Breadcrumb
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
        verbose_name="lenkjenamn",
        populate_from="title",
        unique_with="parent",
        editable=True,
    )

    def path(self):
        """Returns a /-separated list of ancestor slugs, including self."""
        slugs = [ancestor.slug for ancestor in self.ancestors(include_self=True)]
        return "/".join(slugs)

    def breadcrumbs(self, include_self=False) -> list[Breadcrumb]:
        return [
            Breadcrumb(ancestor.get_absolute_url(), ancestor.title)
            for ancestor in self.ancestors(include_self=include_self)
        ]

    def get_absolute_url(self):
        return reverse("articles:ArticleDetail", args=[self.path()])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "slug"], name="unique_slug")
        ]
        ordering = ["title"]
        verbose_name = "artikkel"
        verbose_name_plural = "artiklar"
