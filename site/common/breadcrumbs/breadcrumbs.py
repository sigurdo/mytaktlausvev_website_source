"""
breadcrumbs.py

Main components of the breadcrumbs system.

Documentation for the breadcrumbs system can be found at https://gitlab.com/taktlause/taktlausveven/-/wikis/Breadcrumbs
"""

from dataclasses import dataclass

from django.views.generic import View


@dataclass(eq=True, frozen=True)
class Breadcrumb:
    """
    Standardized breadcrumb designed to work with `BreadcrumbsMixin` and `common/breadcrumbs/breadcrumbs.html`.

    `str` `url`: The URL the breadcrumb should redirect to
    `str` `label`: The breadcrumb's label
    """

    url: str
    label: str


class BreadcrumbsMixin(View):
    breadcrumb_parent: View = None

    @classmethod
    def get_breadcrumb_parent(cls, **kwargs) -> View:
        return cls.breadcrumb_parent

    @classmethod
    def get_breadcrumb(cls, **kwargs) -> Breadcrumb:
        """Must be overriden to return a `Breadcrumb`."""
        raise NotImplementedError(
            "BreadcrumbsMixin.get_breadcrumb() must be overridden"
        )

    @classmethod
    def get_breadcrumbs_from_parent(cls, **kwargs) -> list:
        parent = cls.get_breadcrumb_parent(**kwargs)
        if parent is None:
            return []
        return parent.get_breadcrumbs_for_children(**kwargs)

    @classmethod
    def get_breadcrumbs_for_children(cls, **kwargs) -> list:
        return [
            *cls.get_breadcrumbs_from_parent(**kwargs),
            cls.get_breadcrumb(**kwargs),
        ]

    def get_breadcrumbs_kwargs(self) -> dict:
        return {}

    def get_breadcrumbs(self) -> list:
        return self.get_breadcrumbs_from_parent(**self.get_breadcrumbs_kwargs())

    def get_context_data(self, **kwargs):
        kwargs["breadcrumbs"] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)
