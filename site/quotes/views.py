from django.shortcuts import render
from quotes.models import Quote
import datetime
from .forms import QuoteForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

@login_required
def new_quote(request):
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
