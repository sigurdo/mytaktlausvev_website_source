import inspect
from dataclasses import dataclass

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import View


@dataclass(eq=True, frozen=True)
class Breadcrumb:
    """
    Standardized breadcrumb designed to work with `BreadcrumbsMixin` and `common/breadcrumbs/breadcrumbs.html`.

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


class NestingBreadcrumbsMixin(BreadcrumbsMixin):
    """
    A mixin that can be used on a set of class-based views to generate a coherent breadcrumb hierarchy with minimal code.

    Documentation: https://gitlab.com/taktlause/taktlausveven/-/wikis/Breadcrumbs.
    """

    """The class of the "parent" view of the current view, in the breadcrumbs hierarchy."""
    nesting_breadcrumb_parent = None

    """Keywordarguments for the the `__init__` method of the parent view."""
    nesting_breadcrumb_parent_initkwargs = {}

    """Positional arguments for the parent view."""
    nesting_breadcrumb_parent_args = []

    """
    When set to `True`, `self.kwargs` will be used used as keywordarguments for the parent view.
    This behaviour will be overridden by defining `nesting_breadcrumb_parent_kwargs`.
    """
    nesting_breadcrumb_parent_kwargs_same = False

    """Keywordarguments for the parent view."""
    nesting_breadcrumb_parent_kwargs = None

    """
    Title of the breadcrumb for the current view.
    This is only used if the view is the parent of another view that uses nesting breadcrumbs.
    """
    nesting_breadcrumb_title = None

    """
    Name of the URL pattern of the current view.
    This is only used if the view is the parent of another view that uses nesting breadcrumbs.
    There is usually not necessary to configure it, since `get_nesting_breadcrumb_url_name()`
    guesses it if it is not given. The guess is based on name and location of the class.
    """
    nesting_breadcrumb_url_name = None

    def get_nesting_breadcrumb_parent(self):
        return self.nesting_breadcrumb_parent

    def get_nesting_breadcrumb_parent_initkwargs(self):
        return self.nesting_breadcrumb_parent_initkwargs

    def get_nesting_breadcrumb_parent_args(self):
        return self.nesting_breadcrumb_parent_args

    def get_nesting_breadcrumb_parent_kwargs_same(self):
        return self.nesting_breadcrumb_parent_kwargs_same

    def get_nesting_breadcrumb_parent_kwargs(self):
        if self.nesting_breadcrumb_parent_kwargs:
            return self.nesting_breadcrumb_parent_kwargs
        if self.get_nesting_breadcrumb_parent_kwargs_same():
            return self.kwargs
        return {}

    def get_nesting_breadcrumb_title(self):
        if not self.nesting_breadcrumb_title:
            raise NotImplementedError(
                f"`nesting_breadcrumb_title` not defined for {self.__class__.__name__}"
            )
        return self.nesting_breadcrumb_title

    def get_nesting_breadcrumb_url_name(self):
        if self.nesting_breadcrumb_url_name:
            return self.nesting_breadcrumb_url_name
        app_name = inspect.getmodule(self.__class__).__name__.split(".")[0]
        view_name = self.__class__.__name__
        url_name = f"{app_name}:{view_name}"
        try:
            reverse(url_name, kwargs=self.kwargs)
        except NoReverseMatch:
            raise NotImplementedError(
                f"`nesting_breadcrumb_url_name` not defined for {self.__class__.__name__} and the guessed URL name `{url_name}` with following kwargs: {self.kwargs} had no match"
            )
        return url_name

    def get_breadcrumbs_for_children(self):
        return [
            *self.get_breadcrumbs(),
            Breadcrumb(
                url=reverse(
                    self.get_nesting_breadcrumb_url_name(),
                    kwargs=self.kwargs,
                ),
                name=self.get_nesting_breadcrumb_title(),
            ),
        ]

    def get_breadcrumbs(self):
        if self.nesting_breadcrumb_parent is None:
            return []
        parent = self.get_nesting_breadcrumb_parent()(
            **self.get_nesting_breadcrumb_parent_initkwargs()
        )
        parent.setup(
            self.request,
            *self.get_nesting_breadcrumb_parent_args(),
            **self.get_nesting_breadcrumb_parent_kwargs(),
        )
        if hasattr(parent, "get_object"):
            parent.object = parent.get_object()
        return parent.get_breadcrumbs_for_children()
