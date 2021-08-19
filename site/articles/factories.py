import factory
from accounts.factories import UserFactory
from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = "Article"
    description = "This is an article."
    created_by = factory.SubFactory(UserFactory)
