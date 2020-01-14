from django.shortcuts import render
from quotes.models import Quote
import datetime

def all_quotes(request):
    # lager dummy-sitat til testing
    # n = Quote(title="Test", text="Test text 123", timestamp=datetime.datetime.now())
    # n.save()
    print(Quote.objects.all())
    return render(
        request,
        "quotes/quotes.html",
        {
            "quotes": Quote.objects.all()
        }
    )