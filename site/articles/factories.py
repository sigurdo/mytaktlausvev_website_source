import factory

from accounts.factories import UserFactory

from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = "Article"
    content = "This is an article."
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
