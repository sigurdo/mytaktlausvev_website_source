from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.urls import reverse

from accounts.models import UserCustom
from articles.factories import ArticleFactory
from common.embeddable_text.factories import EmbeddableTextFactory
from contact.factories import ContactCategoryFactory
from instruments.factories import InstrumentGroupFactory, InstrumentTypeFactory
from navbar.factories import NavbarItemFactory
from navbar.models import NavbarItem


class Command(BaseCommand):
    def handle(self, **options):
        Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={"domain": "(MYTAKTLAUSVEV_VARIABLE(domain))", "name": "main"},
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

Du har nå satt opp ein vevside for (MYTAKTLAUSVEV_VARIABLE(appearance.orchestra_name)). Her finn du nokre tips for å kome i gang.

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
            content='Hei og velkomen til (MYTAKTLAUSVEV_VARIABLE(appearance.orchestra_name))! Brukarnamnet ditt er "{{ username }}".',
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

        group_flute = InstrumentGroupFactory(name="Fløyte")
        group_clarinet = InstrumentGroupFactory(name="Klarinett")
        group_trumpet = InstrumentGroupFactory(name="Trompet")
        group_horn = InstrumentGroupFactory(name="Horn")
        group_saxophone = InstrumentGroupFactory(name="Saksofon")
        group_trombone = InstrumentGroupFactory(name="Trombone")
        group_euphonium = InstrumentGroupFactory(name="Eufonium")
        group_tuba = InstrumentGroupFactory(name="Tuba")
        group_percussion = InstrumentGroupFactory(name="Slagverk")
        group_conductor = InstrumentGroupFactory(name="Dirigent")
        group_other = InstrumentGroupFactory(name="Anna")
        group_string = InstrumentGroupFactory(name="Strykeinstrument")
        group_guitar = InstrumentGroupFactory(name="Gitar")

        InstrumentTypeFactory(
            name="Pikkolo",
            group=group_flute,
            detection_keywords=[
                "pikkolo",
                "piccolo",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Fløyte",
            group=group_flute,
            detection_keywords=[
                "flute",
                "fløyte",
                "flauta",
                "phloitte",
            ],
            detection_exceptions=[
                "piccolo",
                "pikkolo",
            ],
        )
        InstrumentTypeFactory(
            name="Obo",
            group=group_flute,
            detection_keywords=[
                "oboe",
                "obo",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Klarinett",
            group=group_clarinet,
            detection_keywords=[
                "klarinet",
                "clarinet",
                "clarinete",
                "lakris",
                "lakriids",
            ],
            detection_exceptions=[
                "bass",
                "alt",
                "eb",
                "boeugd-guld-lakriids",
            ],
        )
        InstrumentTypeFactory(
            name="Bassklarinett",
            group=group_clarinet,
            detection_keywords=[
                "bassklarinet",
                "bass klarinet",
                "bass clarinet",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Altklarinett",
            group=group_clarinet,
            detection_keywords=[
                "altklarinet",
                "alto clarinet",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Eb-klarinett",
            group=group_clarinet,
            detection_keywords=[
                "eb clarinet",
                "eb-clarinet",
                "eb-klarinet",
                "eb klarinet",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Fagott",
            group=group_clarinet,
            detection_keywords=[
                "bassoon",
                "fagott",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Trompet",
            group=group_trumpet,
            detection_keywords=[
                "trumpet",
                "trompet",
                "trompeta",
                "fliscorno",
                "fliscomo",
                "trompang",
            ],
            detection_exceptions=[
                "bass-trompang",
            ],
        )
        InstrumentTypeFactory(
            name="Kornett",
            group=group_trumpet,
            detection_keywords=[
                "kornett",
                "komett",
                "cornet",
                "comet",
                "chornæt",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Tenorhorn",
            group=group_horn,
            detection_keywords=[
                "tenororn",
                "tenorhom",
                "bb-horn",
                "bb horn",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Sopransaksofon",
            group=group_saxophone,
            detection_keywords=[
                "sopransaks",
                "sopransax",
                "sopransaxofon",
                "sopransaksofon",
                "soprano saxophone",
                "soprano sax",
                "saxo soprano",
            ],
            detection_exceptions=[
                "sopran",
                "tenor",
                "baryton",
                "baritone",
                "barítono",
            ],
        )
        InstrumentTypeFactory(
            name="Altsaksofon",
            group=group_saxophone,
            detection_keywords=[
                "altsax",
                "altsaxofon",
                "saxofon",
                "altsaks",
                "altsaksofon",
                "saksofon",
                "saxophone",
                "alto saxophone",
                "alto sax",
                "saxo alto",
                "alt-boeugd-guld-lakriids",
            ],
            detection_exceptions=[
                "sopran",
                "tenor",
                "baryton",
                "baritone",
                "barítono",
            ],
        )
        InstrumentTypeFactory(
            name="Tenorsaksofon",
            group=group_saxophone,
            detection_keywords=[
                "tenorsaks",
                "tenorsaksofon",
                "tenorsax",
                "tenorsaxofon",
                "tenor sax",
                "saxo tenore",
                "tenor-boeugd-guld-lakriids",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Barytonsaksofon",
            group=group_saxophone,
            detection_keywords=[
                "barytonsaxofon",
                "barytonsaksofon",
                "barysax",
                "barysaks",
                "saxo barítono",
                "baritone saxophone",
                "baritone sax",
                "bariton-boeugd-guld-lakriids",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Trombone",
            group=group_trombone,
            detection_keywords=[
                "trombone",
                "trombón",
                "trækbasun",
            ],
            detection_exceptions=[
                "sopran",
                "bass",
            ],
        )
        InstrumentTypeFactory(
            name="Soprantrombone",
            group=group_trombone,
            detection_keywords=[
                "soprantrombone",
                "soprano trombone",
                "trombón soprano",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Basstrombone",
            group=group_trombone,
            detection_keywords=[
                "basstrombone",
                "bass trombone",
                "trombón basso",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Eufonium",
            group=group_euphonium,
            detection_keywords=[
                "eufonium",
                "euphonium",
                "juff",
                "reiisetuba",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Baryton",
            group=group_euphonium,
            detection_keywords=[
                "baryton",
                "baritone",
                "bombardíno",
            ],
            detection_exceptions=[
                "barytonsaxofon",
                "barytonsaksofon",
                "baritone sax",
            ],
        )
        InstrumentTypeFactory(
            name="Tuba",
            group=group_tuba,
            detection_keywords=[
                "tuba",
                "bass",
                "eb-tuba",
                "eb tuba",
                "bb-tuba",
                "bb tuba",
                "bass-trompang",
            ],
            detection_exceptions=[
                "trombone",
                "clarinet",
                "klarinett",
                "guitar",
                "bassoon",
                "el-bass",
                "el bass",
                "electric bass",
                "string bass",
                "bass drum",
                "reiisetuba",
            ],
        )
        InstrumentTypeFactory(
            name="Slagverk",
            group=group_percussion,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Skarptromme",
            group=group_percussion,
            detection_keywords=[
                "caja",
                "snare drum",
                "skarptromme",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Stortromme",
            group=group_percussion,
            detection_keywords=[
                "stortromme",
                "bass drum",
                "basstromme",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Cymbal",
            group=group_percussion,
            detection_keywords=[
                "cymbal",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Kubjelle",
            group=group_percussion,
            detection_keywords=[
                "kubjelle",
                "cow bell",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Tamburin",
            group=group_percussion,
            detection_keywords=[
                "pandereta",
                "tamburin",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Triangel",
            group=group_percussion,
            detection_keywords=[
                "triangel",
                "triangle",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Pauker",
            group=group_percussion,
            detection_keywords=[
                "pauk",
                "timpani",
                "timbales",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Perkusjon",
            group=group_percussion,
            detection_keywords=[
                "slagverk",
                "perkusjon",
                "percussion",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Tom-toms",
            group=group_percussion,
            detection_keywords=[
                "tom-tom",
                "tom tom",
                "trio tom",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Harpe",
            group=group_other,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Orgel",
            group=group_other,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Soprankornett",
            group=group_trumpet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Piano",
            group=group_other,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Fele",
            group=group_string,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Bratsj",
            group=group_string,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Cello",
            group=group_string,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Pikkoloobo",
            group=group_flute,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Kontrabass",
            group=group_string,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Mellofon",
            group=group_trumpet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Kontrabassklarinett",
            group=group_clarinet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Susafon",
            group=group_tuba,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Synthesizer",
            group=group_other,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Bongotrommer",
            group=group_percussion,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Tenortuba",
            group=group_tuba,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Ukjend",
            group=group_other,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Marakas",
            group=group_percussion,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Melodisk slagverk",
            group=group_percussion,
            detection_keywords=[
                "melodisk",
                "mallets",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Bassaksofon",
            group=group_saxophone,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Pikkolotrompet",
            group=group_trumpet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Quad-trommer",
            group=group_percussion,
            detection_keywords=[
                "quad tom",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Basstrompet",
            group=group_trumpet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Engelsk horn",
            group=group_flute,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Quint-trommer",
            group=group_percussion,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Xylofon",
            group=group_percussion,
            detection_keywords=[
                "xylophone",
                "xylofon",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Marimba",
            group=group_percussion,
            detection_keywords=[
                "marimba",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Vibrafon",
            group=group_percussion,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Kontrafagott",
            group=group_clarinet,
            detection_keywords=[],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Althorn",
            group=group_horn,
            detection_keywords=[
                "althorn",
                "althom",
                "eb-horn",
                "eb horn",
                "ephterslags-speciialiist eb",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Ambolt",
            group=group_percussion,
            detection_keywords=[
                "ambolt",
                "anvil",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Banjo",
            group=group_other,
            detection_keywords=[
                "banjo",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Valthorn",
            group=group_horn,
            detection_keywords=[
                "horn",
                "hom",
                "trompa",
                "f-horn",
                "f horn",
                "ephterslags-speciialiist",
                "valthorn",
            ],
            detection_exceptions=[
                "althorn",
                "althom",
                "eb-horn",
                "eb horn",
                "tenororn",
                "tenorhom",
                "bb-horn",
                "bb horn",
                "ephterslags-speciialiist eb",
            ],
        )
        InstrumentTypeFactory(
            name="Flygelhorn",
            group=group_trumpet,
            detection_keywords=[
                "flugelhorn",
                "flugelhom",
                "flygelhorn",
                "flygelhom",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Klokkespill",
            group=group_percussion,
            detection_keywords=[
                "klokkespill",
                "lyre",
                "lyra",
                "bells",
                "glockenspiel",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Vaskebrett",
            group=group_percussion,
            detection_keywords=[
                "vaskebrett",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Bassgitar",
            group=group_guitar,
            detection_keywords=[
                "bass guitar",
                "el-bass",
                "el bass",
                "electric bass",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Gitar",
            group=group_guitar,
            detection_keywords=[
                "guitar",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Partitur",
            group=group_conductor,
            detection_keywords=[
                "partitur",
                "score",
                "conductor",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Conga",
            group=group_percussion,
            detection_keywords=[
                "conga",
            ],
            detection_exceptions=[],
        )
        InstrumentTypeFactory(
            name="Trommesett",
            group=group_percussion,
            detection_keywords=[
                "tromme",
                "drum",
                "trommesett",
                "drum set",
                "drumset",
                "platos y campanas",
            ],
            detection_exceptions=[
                "caja",
                "snare drum",
                "skarptromme",
                "stortromme",
                "bass",
                "conga",
                "conga drum",
            ],
        )
        InstrumentTypeFactory(
            name="Vokal",
            group=group_other,
            detection_keywords=[
                "vokal",
                "vocal",
                "voice",
            ],
            detection_exceptions=[],
        )
