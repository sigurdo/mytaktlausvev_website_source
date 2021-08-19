from django.views.generic.detail import DetailView
from .models import Article


class ArticleDetail(DetailView):
    """View for viewing an article."""

    model = Article