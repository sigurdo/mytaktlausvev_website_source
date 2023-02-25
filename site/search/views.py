from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET
from watson.search import search

from .forms import SearchForm


@require_GET
@login_required
def search_view(request):
    template = (
        "search/partials/search_results.html"
        if request.headers.get("Hx-Request")
        else "search/search.html"
    )

    return render(
        request,
        template,
        {
            "search_results": search(request.GET.get("query", ""))[:50],
            "form": SearchForm,
        },
    )
