from django.core.management.base import BaseCommand
from accounts.models import UserCustom
from articles.factories import ArticleFactory


class Command(BaseCommand):
    def handle(self, **options):
        superuser = UserCustom.objects.create_superuser(
            "leiar", "leiar@taktlaus.no", "password"
        )
        ArticleFactory(
            title="Om oss",
            content="Dette er ein artikkel om oss",
            public=True,
            comments_allowed=False,
            created_by=superuser,
            modified_by=superuser,
        ).save()
        songar = ArticleFactory(
            title="Songar",
            content="Eit knippe songar.",
            public=True,
            comments_allowed=True,
            created_by=superuser,
            modified_by=superuser,
        )
        songar.save()
        ArticleFactory(
            title="Calypso",
            content="Tanken går til den skjønne vår\nda jeg sang i mannskoret Polyfon,\ntil den turne da vi dro avsted\nmed lokaltog fra Trondheims sentralstasjon.",
            public=True,
            comments_allowed=True,
            created_by=superuser,
            modified_by=superuser,
            parent=songar,
        ).save()
        ArticleFactory(
            title="Wiki",
            content="Informasjon til Taktlause.",
            public=True,
            comments_allowed=True,
            created_by=UserCustom.objects.get(username="leiar"),
            modified_by=UserCustom.objects.get(username="leiar"),
        ).save()
