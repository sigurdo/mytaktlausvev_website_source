"""Views for quotes-app"""
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from quotes.models import Quote
from .forms import QuoteForm


@login_required
def new_quote(request):
    """View-function for new-quote-form"""
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.timestamp = datetime.datetime.now()
            quote.save()
            return HttpResponseRedirect("/sitat/")
    elif request.method == "GET":
        form = QuoteForm()
        return render(request, "quotes/new_quote.html", {"form": form})


def quotes(request):
    """View-function for displaying all quotes"""
    paginator = Paginator(Quote.objects.all(), 2)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "quotes/quotes.html",
        {
            "quotes": page
        }
    )
