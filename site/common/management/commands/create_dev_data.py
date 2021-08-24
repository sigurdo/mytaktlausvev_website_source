from django.core.management.base import BaseCommand
from accounts.models import UserCustom
from articles.factories import ArticleFactory

class Command(BaseCommand):
    def handle(self, **options):
        superuser = UserCustom.objects.create_superuser("leiar", "leiar@taktlaus.no", "password")
        ArticleFactory(
            title="Om oss",
            description="Dette er ein artikkel om oss",
            public=True,
            comments_allowed=False,
            created_by=superuser,
            modified_by=superuser
        ).save()
