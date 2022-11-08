from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.urls import reverse

from accounts.models import UserCustom
from articles.factories import ArticleFactory
from common.embeddable_text.factories import EmbeddableTextFactory
from contact.factories import ContactCategoryFactory
from navbar.factories import NavbarItemFactory
from navbar.models import NavbarItem


class Command(BaseCommand):
    def handle(self, **options):
        Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={"domain": "localhost:8000", "name": "localhost"},
        )

        superuser = UserCustom.objects.create_superuser(
            "(MYTAKTLAUSVEV_VARIABLE(initial_data.superuser.username))",
            "(MYTAKTLAUSVEV_VARIABLE(initial_data.superuser.email))",
            "(MYTAKTLAUSVEV_VARIABLE(initial_data.superuser.password))",
        )
        article_about = ArticleFactory(
            title="Om oss",
            content="",
            public=True,
            comments_allowed=False,
            created_by=superuser,
            modified_by=superuser,
        )
        article_wiki = ArticleFactory(
            title="Wiki",
            content="",
            public=False,
            comments_allowed=True,
            created_by=superuser,
            modified_by=superuser,
        )
        ArticleFactory(
            title="Kom i gang",
            content=f"""
Gratulerer!

Du har nå satt opp ein vevside for (MYTAKTLAUSVEV_VARIABLE(initial_data.orchestra_name)). Her finn du nokre tips for å kome i gang.

## Lage brukarar

Du kan lage fleire brukarar under [{reverse("accounts:UserCustomCreate")}]({reverse("accounts:UserCustomCreate")}).

## Administrasjonspanel

Du kan gjere veldig mykje i administrasjonspanelet ([{reverse("admin:index")}]({reverse("admin:index")})), mellom anna:

### Endre navigasjonslina

Under [Administrasjon](/admin/) > [Navigasjonslinepunkt](/admin/navbar/navbaritem/) ser du oversikta over alle toppnivå-navigasjonslinepunkta. Ved å klikke deg inn på kvart av dei kan du redigere kva dei skal hete og kva dei skal peike til. Om "Type" vert sett til "Nedfallsmeny" vil navigasjonslinepunktet ikkje peike til den angjevne lenkjepeikaren, men vil i staden bli ein nedfallsmeny som viser underpunkta. Desse underpunkta kan du redigere i "Underpunkt"-tabellen.

Eit navigasjonslinepunkt kan kreve innlogging. Dette gjer at navigasjonslinepunktet ikkje er synleg når ein ikkje er logga inn. Om alle underpunkta til ein nedfallsmeny krever innlogging vil heile nedfallsmenyen automatisk verte usynleg når ein ikkje er logga inn.

### Endre innbyggbare tekstar

Innbyggbare tekstar er ein samling av diverse tekstar som vert bygd inn på ulike stader i nettsida, som f. eks. innhaldet i velkomsteposten som automatisk vert sendt ut når ein ny brukar vert oppretta. Desse kan du redigere under [Adminstrasjon](/admin/) > [Innbyggbare tekstar](/admin/embeddable_text/embeddabletext/)

""",
            public=False,
            comments_allowed=True,
            created_by=superuser,
            modified_by=superuser,
            parent=article_wiki,
        )

        ContactCategoryFactory(
            name=superuser.username,
            email=superuser.email,
        )

        about_dropdown = NavbarItemFactory(
            text="Om oss",
            order=0,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Om oss",
            link=article_about.get_absolute_url(),
            order=1,
            parent=about_dropdown,
        )
        NavbarItemFactory(
            text="Kontakt oss",
            link=reverse("contact:ContactView"),
            order=2,
            requires_login=False,
            parent=about_dropdown,
        )
        NavbarItemFactory(
            text="Hendingar",
            link=reverse("events:EventList"),
            order=1,
            requires_login=True,
        )
        sheetmusic_dropdown = NavbarItemFactory(
            text="Notar",
            order=2,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Alle notar",
            link=reverse("sheetmusic:ScoreList"),
            order=1,
            requires_login=True,
            parent=sheetmusic_dropdown,
        )
        NavbarItemFactory(
            text="Repertoar",
            link=reverse("repertoire:ActiveRepertoires"),
            order=2,
            requires_login=True,
            parent=sheetmusic_dropdown,
        )
        photo_dropdown = NavbarItemFactory(
            text="Foto",
            order=2.5,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Fotoarkiv",
            link=reverse("pictures:GalleryList"),
            order=1,
            requires_login=True,
            parent=photo_dropdown,
        )
        NavbarItemFactory(
            text="Nyaste bilete",
            link=reverse("pictures:NewestImagesList"),
            order=2,
            requires_login=True,
            parent=photo_dropdown,
        )
        NavbarItemFactory(
            text="Nytt galleri",
            link=reverse("pictures:GalleryCreate"),
            order=3,
            requires_login=True,
            parent=photo_dropdown,
        )
        other_dropdown = NavbarItemFactory(
            text="Meir",
            order=3,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Sitat",
            link=reverse("quotes:QuoteList"),
            order=2,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Wiki",
            link=article_wiki.get_absolute_url(),
            order=2.5,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Referat",
            link=reverse("minutes:MinutesList"),
            order=2.55,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Brukarfiler",
            link=reverse("user_files:FileList"),
            order=2.57,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Avstemmingar",
            link=reverse("polls:PollList"),
            order=2.58,
            requires_login=False,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Forum",
            link=reverse("forum:ForumList"),
            order=2.6,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Julekalender",
            link=reverse("advent_calendar:AdventCalendarList"),
            order=2.7,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Buttonpdfgenerator",
            link=reverse("buttons:ButtonsView"),
            order=3,
            parent=other_dropdown,
        )
        admin_dropdown = NavbarItemFactory(
            text="Administrasjon",
            order=4,
            type=NavbarItem.Type.DROPDOWN,
            requires_login=True,
        )
        NavbarItemFactory(
            text="Administrasjonspanel",
            link=reverse("admin:index"),
            order=1,
            requires_login=True,
            parent=admin_dropdown,
        )
        NavbarItemFactory(
            text="Instrument",
            link=reverse("instruments:InstrumentList"),
            order=2,
            requires_login=True,
            parent=admin_dropdown,
        )
        NavbarItemFactory(
            text="Uniformar",
            link=reverse("uniforms:JacketList"),
            order=3,
            requires_login=True,
            parent=admin_dropdown,
        )
        NavbarItemFactory(
            text="Opprett artikkel",
            link=reverse("articles:ArticleCreate"),
            order=4,
            requires_login=True,
            parent=admin_dropdown,
        )
        NavbarItemFactory(
            text="Deling av bilete",
            link=reverse("accounts:ImageSharingConsentList"),
            order=6,
            requires_login=True,
            parent=admin_dropdown,
            permissions=["accounts.view_image_sharing_consent"],
        )
        NavbarItemFactory(
            text="Ny brukar",
            link=reverse("accounts:UserCustomCreate"),
            order=7,
            requires_login=True,
            parent=admin_dropdown,
            permissions=["accounts.add_usercustom"],
        )
        NavbarItemFactory(
            text="Søk",
            link=reverse("search:Search"),
            order=6,
            type=NavbarItem.Type.LINK,
        )

        EmbeddableTextFactory(
            name="Framgangsmåte for buttonpdfgenerator",
            content="""
## Framgangsmåte

1. Design nokre motiv du vil lage buttons av. Designet må vere like langt som det er breidt (om ikkje vert det strekt) og ikkje ha noke viktig motiv utanfor sirkelen med sentrum midt i motivet og diameter lik breidda/høgda (om ikkje vert det borte).
2. Last opp motiva her som bilete og oppgje kor mange buttons du ynskjer av kvart motiv. Om du skal lage buttons i ei anna storleik enn Dei Taktlause sin standard, endre ynskja diameter.
3. Trykk generer PDF, vent til sida svarar (dette kan ta nokre sekund om du provar å lage mange eller store buttons) og print ut.
""",
        )
        EmbeddableTextFactory(
            name="Kontakt oss",
            content="Her kan du kontakta dei i styret, eller tillitsvalde. Om du vil vere med oss å spele, gjerne legg til kva instrument du spelar, og om du vil låne instrument.",
        )
        EmbeddableTextFactory(
            name="Kontakt oss - Suksess",
            content="Me har motteke meldinga di, og vil svare så fort me kan.",
        )
        EmbeddableTextFactory(
            name="400",
            content="Dårleg førespurnad, prøv på nytt.",
        )
        EmbeddableTextFactory(
            name="403",
            content="Du har ikkje løyve til å sjå denne sida.",
        )
        EmbeddableTextFactory(
            name="404",
            content="Kunne ikkje finne denne sida.",
        )
        EmbeddableTextFactory(
            name="500",
            content=f"Tenarfeil! Send ein epost snarast til {superuser.username} på {superuser.email}",
        )
        EmbeddableTextFactory(
            name="Velkomenepost",
            content='Hei og velkomen til (MYTAKTLAUSVEV_VARIABLE(initial_data.orchestra_name))! Brukarnamnet ditt er "{{ username }}".',
        )
        EmbeddableTextFactory(
            name="Stemmeredigeringstips",
            content="Her kan ein redigere stemmane til denne nota.",
        )
        EmbeddableTextFactory(
            name="Kalenderintegrasjonsknapp hjelpetekst",
            content='Sjå etter legg til kalender frå nettadresse" eller "abonner på kalender" i kalenderappen din. Dette er vanlegvis ikkje det same som "importer kalenderfil". "importer kalenderfil" importerar bare hendingane ein gong, og så må du gjere dette om att kvar gong det kjem nye hendingar. I mange kalenderappar er dette ikkje mogleg å gjere direkte i kalender-appen, og ein må gjere det via t.d. ein Google- eller Outlook-konto.',
        )
        EmbeddableTextFactory(
            name="Nykelinfo-hjelpetekst for hendingar",
            content="""
Her kan du skrive nykelinformasjon om hendinga. Oppføringane du skriv vil verte vist oppramsa med kolon som vist nedanfor. Oppføringar med lik rekkjefølgje vert sortert alfabetisk.

---

**Nykel:** Info
**Anna nykel:** Anna info

---
""",
        )
        EmbeddableTextFactory(
            name="Buttonmotivbibliotek", content="Her finn du ferdiglaga buttonmotiv!"
        )
