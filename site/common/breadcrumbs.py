from dataclasses import dataclass, field

from django.views.generic import View


@dataclass(eq=True, frozen=True)
class Breadcrumb:
    """
    Standardized breadcrumb designed to work with `BreadcrumbsMixin` and `common/includes/breadcrumbs.html`.

    `str` `url`: The URL the breadcrumb should redirect to
    `str` `name`: The breadcrumb's label
    """

    url: str
    name: str


class BreadcrumbsMixin(View):
    def get_breadcrumbs(self) -> list:
        """Must be overriden to return a list of `Breadcrumb`s."""
        raise NotImplementedError(
            "BreadcrumbsMixin.get_breadcrumbs() must be overridden"
        )

    def get_context_data(self, **kwargs):
        kwargs["breadcrumbs"] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)
