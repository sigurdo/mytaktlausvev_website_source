from django.shortcuts import render
from quotes.models import Quote
import datetime
from .forms import QuoteForm
from django.http import HttpResponseRedirect

def quotes(request):
    # lager dummy-sitat til testing
    if request.user.is_authenticated and request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.timestamp = datetime.datetime.now()
            quote.save()
            return HttpResponseRedirect("/sitat/")
    elif request.method == "GET":
        form = QuoteForm()
    else:
        return HttpResponseRedirect("/")
    
    return render(
        request,
        "quotes/quotes.html",
        {
            "quotes": Quote.objects.all(),
            "form": form
        }
    )
