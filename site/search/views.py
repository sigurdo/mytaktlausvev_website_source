from django.contrib.auth.mixins import LoginRequiredMixin
from watson.views import SearchView

from search.forms import SearchForm


class Search(LoginRequiredMixin, SearchView):
    template_name = "search/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(initial={"q": context["query"]})
        return context
