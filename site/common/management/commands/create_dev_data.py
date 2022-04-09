from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils.timezone import make_aware

from accounts.models import UserCustom
from articles.factories import ArticleFactory
from comments.factories import CommentFactory
from common.test_utils import test_pdf_multipage
from contact.factories import ContactCategoryFactory
from events.factories import EventAttendanceFactory, EventFactory
from events.models import Attendance
from forum.factories import ForumFactory, TopicFactory
from instruments.factories import (
    InstrumentFactory,
    InstrumentGroupFactory,
    InstrumentLocationFactory,
    InstrumentTypeFactory,
)
from instruments.models import Instrument
from minutes.factories import MinutesFactory
from navbar.factories import NavbarItemFactory
from navbar.models import NavbarItem
from pictures.factories import GalleryFactory, ImageFactory
from polls.factories import ChoiceFactory, PollFactory, VoteFactory
from repertoire.factories import RepertoireEntryFactory, RepertoireFactory
from sheetmusic.factories import (
    FavoritePartFactory,
    PartFactory,
    PdfFactory,
    ScoreFactory,
)
from uniforms.factories import JacketFactory, JacketLocationFactory, JacketUserFactory
from uniforms.models import Jacket


class Command(BaseCommand):
    def handle(self, **options):
        Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={"domain": "localhost:8000", "name": "localhost"},
        )

        leader = UserCustom.objects.create_superuser(
            "leiar",
            "leiar@taktlaus.no",
            "password",
            name="Leiar Leiarsen",
            birthdate=date(2012, 12, 12),
            student_card_number="42069420",
            phone_number="12345678",
            address="The Milky Way",
            home_page="https://example.com",
            membership_period="Haust, 1337 -",
        )
        aspirant = UserCustom.objects.create_user(
            "aspirant",
            "aspirant@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.ASPIRANT,
            light_mode=True,
        )
        member = UserCustom.objects.create_user(
            "medlem",
            "medlem@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.PAYING,
        )
        retiree = UserCustom.objects.create_user(
            "pensjonist",
            "pensjonist@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.RETIRED,
        )
        musical_leader = UserCustom.objects.create_user(
            "musikalsk",
            "muikalsk@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.PAYING,
        )

        article_about = ArticleFactory(
            title="Om oss",
            content="Dette er ein artikkel om oss",
            public=True,
            comments_allowed=False,
            created_by=leader,
            modified_by=leader,
        )
        article_songs = ArticleFactory(
            title="Songar",
            content="Eit knippe songar.",
            public=True,
            comments_allowed=True,
            created_by=leader,
            modified_by=leader,
        )
        CommentFactory(
            content_object=article_songs,
            comment="Eg elskar songar!",
            created_by=retiree,
        )
        ArticleFactory(
            title="Calypso",
            content="Tanken går til den skjønne vår\nda jeg sang i mannskoret Polyfon,\ntil den turne da vi dro avsted\nmed lokaltog fra Trondheims sentralstasjon.",
            public=True,
            comments_allowed=True,
            created_by=leader,
            modified_by=leader,
            parent=article_songs,
        )
        article_wiki = ArticleFactory(
            title="Wiki",
            content="Informasjon til Taktlause.",
            public=True,
            comments_allowed=True,
            created_by=leader,
            modified_by=leader,
        )
        ArticleFactory(
            title="Kalenderfeed-vegvisar",
            content="Importer kalenderfeeden frå [denne](/hendingar/taktlaushendingar.ics) lenkja i kalender-appen din og sett han opp til å oppdatere seg automatisk.",
            public=True,
            comments_allowed=False,
            created_by=leader,
            modified_by=leader,
        )

        ContactCategoryFactory(name="Generelt")
        ContactCategoryFactory(name="Bli med!")

        event = EventFactory(
            title="SMASH",
            content="SMASH in Trondheim",
            created_by=leader,
            modified_by=leader,
            start_time=make_aware(datetime.now() + timedelta(365)),
        )
        EventAttendanceFactory(event=event, person=leader, status=Attendance.ATTENDING)
        EventAttendanceFactory(event=event, person=member, status=Attendance.ATTENDING)
        EventAttendanceFactory(
            event=event, person=aspirant, status=Attendance.ATTENDING_MAYBE
        )
        EventAttendanceFactory(
            event=event, person=retiree, status=Attendance.ATTENDING_NOT
        )
        EventFactory(
            start_time=make_aware(datetime(datetime.now().year + 1, 1, 1)),
            title="Nyttårsfest",
            content="Nyttig for å studere kanttilfelle for starttider.",
        )
        first_wednesday = datetime.combine(date.today(), time(hour=18))
        while first_wednesday.weekday() != 2:
            first_wednesday += timedelta(days=1)
        EventFactory(
            title="Øving",
            content="Vanleg øving.",
            created_by=leader,
            modified_by=leader,
            start_time=make_aware(first_wednesday),
        )
        EventFactory(
            title="Brettspelkveld",
            content="Brettspelkveld i KJL4.",
            created_by=leader,
            modified_by=leader,
            start_time=make_aware(first_wednesday + timedelta(days=1)),
        )
        month = datetime.now().month
        year = datetime.now().year
        datetime_theme_party = datetime(year if month < 8 else year + 1, 3, 1, 18)
        while datetime_theme_party.weekday() != 5:
            datetime_theme_party += timedelta(days=1)
        datetime_theme_party += timedelta(days=7)
        EventFactory(
            title="Temafest",
            content="Ikkje så viktig med tema, men viktig med fest.",
            created_by=leader,
            modified_by=leader,
            start_time=make_aware(datetime_theme_party),
        )
        medal_galla_datetime = datetime(year - 1 if month < 8 else year, 11, 1, 18)
        while medal_galla_datetime.weekday() != 5:
            medal_galla_datetime += timedelta(days=1)
        EventFactory(
            title="Medaljegalla",
            content="Ete lasagne, drikke ulike drikkar og danse.",
            created_by=leader,
            modified_by=leader,
            start_time=make_aware(medal_galla_datetime),
        )
        flute = InstrumentGroupFactory(name="Fløyte")
        clarinet = InstrumentGroupFactory(name="Klarinett")
        trumpet = InstrumentGroupFactory(name="Trompet")
        horn = InstrumentGroupFactory(name="Horn")
        saxophone = InstrumentGroupFactory(name="Saksofon")
        trombone = InstrumentGroupFactory(name="Trombone")
        juff = InstrumentGroupFactory(name="Eufonium")
        tuba = InstrumentGroupFactory(name="Tuba")
        drums = InstrumentGroupFactory(name="Slagverk")
        synthesizer = InstrumentGroupFactory(name="Synthesizer")
        director = InstrumentGroupFactory(name="Dirigent")
        group_other = InstrumentGroupFactory(name="Anna")

        type_piccolo = InstrumentTypeFactory(name="Pikkolo", group=flute)
        type_flute = InstrumentTypeFactory(name="Fløyte", group=flute)
        InstrumentTypeFactory(name="Obo", group=flute)
        type_clarinet = InstrumentTypeFactory(name="Klarinett", group=clarinet)
        InstrumentTypeFactory(name="Altklarinett", group=clarinet)
        InstrumentTypeFactory(name="Eb-klarinett", group=clarinet)
        InstrumentTypeFactory(name="Bassklarinett", group=clarinet)
        InstrumentTypeFactory(name="Fagott", group=clarinet)
        type_trumpet = InstrumentTypeFactory(name="Trompet", group=trumpet)
        InstrumentTypeFactory(name="Kornett", group=trumpet)
        InstrumentTypeFactory(name="Flugelhorn", group=trumpet)
        InstrumentTypeFactory(name="Horn", group=horn)
        InstrumentTypeFactory(name="Althorn", group=horn)
        InstrumentTypeFactory(name="Tenorhorn", group=horn)
        InstrumentTypeFactory(name="Sopransaksofon", group=saxophone)
        type_saxophone = InstrumentTypeFactory(name="Altsaksofon", group=saxophone)
        InstrumentTypeFactory(name="Tenorsaksofon", group=saxophone)
        InstrumentTypeFactory(name="Barytonsaksofon", group=saxophone)
        type_trombone = InstrumentTypeFactory(name="Trombone", group=trombone)
        InstrumentTypeFactory(name="Soprantrombone", group=trombone)
        InstrumentTypeFactory(name="Basstrombone", group=trombone)
        type_euphonium = InstrumentTypeFactory(name="Eufonium", group=juff)
        InstrumentTypeFactory(name="Baryton", group=juff)
        type_tuba = InstrumentTypeFactory(name="Tuba", group=tuba)
        type_drumset = InstrumentTypeFactory(name="Trommesett", group=drums)
        InstrumentTypeFactory(name="Skarptromme", group=drums)
        InstrumentTypeFactory(name="Stortromme", group=drums)
        InstrumentTypeFactory(name="Tom-toms", group=drums)
        InstrumentTypeFactory(name="Cymbal", group=drums)
        InstrumentTypeFactory(name="Kubjelle", group=drums)
        InstrumentTypeFactory(name="Tamburin", group=drums)
        InstrumentTypeFactory(name="Triangel", group=drums)
        InstrumentTypeFactory(name="Pauker", group=drums)
        InstrumentTypeFactory(name="Perkusjon", group=drums)
        InstrumentTypeFactory(name="Klokkespill", group=drums)
        InstrumentTypeFactory(name="Gitar", group=group_other)
        InstrumentTypeFactory(name="Bassgitar", group=group_other)
        InstrumentTypeFactory(name="Partitur", group=director)
        type_grand_piano = InstrumentTypeFactory(name="Flygel", group=drums)
        type_synthesizer = InstrumentTypeFactory(name="Synthesizer", group=synthesizer)
        type_vco = InstrumentTypeFactory(
            name="Spenningsstyrt oscillator", group=synthesizer
        )
        type_electric_piano = InstrumentTypeFactory(name="EL-piano", group=synthesizer)
        type_loop_station = InstrumentTypeFactory(
            name="Løkkestasjon", group=synthesizer
        )
        main_storage = InstrumentLocationFactory(name="Hovedskapet")
        InstrumentLocationFactory(name="Styreskapet")
        InstrumentLocationFactory(name="Saunaen")
        InstrumentLocationFactory(name="Tatt med hjem")
        member.instrument_type = type_flute
        member.save()
        InstrumentFactory(
            type=type_piccolo, identifier="1", user=member, location=main_storage
        )
        leader.instrument_type = type_synthesizer
        leader.save()
        musical_leader.instrument_type = type_grand_piano
        musical_leader.save()
        InstrumentFactory(
            type=type_trumpet, identifier="piccolo", user=leader, location=main_storage
        )
        InstrumentFactory(
            type=type_tuba,
            identifier="2",
            location=main_storage,
            comment="Valsa over på SMASH",
            state=Instrument.State.UNPLAYABLE,
        )
        jacket_at_home = JacketLocationFactory(
            name="Hjemme",
        )
        jacket_at_storage = JacketLocationFactory(
            name="Jakkeskapet",
        )
        jacket_1 = JacketFactory(
            number=1,
            comment="",
            state=Jacket.State.NEEDS_REPAIR,
            location=jacket_at_storage,
        )
        JacketFactory(
            number=2,
            comment="Mangler 3 knapper og en lomme",
            state=Jacket.State.UNUSABLE,
            location=jacket_at_storage,
        )
        jacket_42 = JacketFactory(
            number=42,
            state=Jacket.State.GOOD,
            location=jacket_at_home,
        )
        jacket_65 = JacketFactory(
            number=65,
            state=Jacket.State.NEEDS_REPAIR,
            location=jacket_at_storage,
        )
        JacketUserFactory(
            user=leader,
            jacket=jacket_65,
        )
        JacketUserFactory(
            user=member,
            jacket=jacket_42,
        )
        JacketUserFactory(
            user=aspirant,
            jacket=jacket_1,
        )
        JacketUserFactory(
            user=retiree,
            jacket=jacket_1,
            is_owner=False,
        )
        JacketUserFactory()
        JacketUserFactory()

        general = ForumFactory(title="General", description="For general stuff.")
        ForumFactory(
            title="Www",
            description="List of things that don't work on the new website.",
        )
        truths = TopicFactory(title="Truths", forum=general, created_by=leader)
        the_device = TopicFactory(title="The Device", forum=general, created_by=member)
        CommentFactory(comment="2+2=5", content_object=truths, created_by=leader)
        CommentFactory(comment="???", content_object=the_device, created_by=member)

        poll = PollFactory(
            question="Beste instrument?",
            created_by=leader,
            modified_by=leader,
            public=True,
        )
        choice_juff = ChoiceFactory(text="Juff", poll=poll)
        choice_tuba = ChoiceFactory(text="Mindre tuba", poll=poll)
        VoteFactory(choice=choice_juff, user=leader)
        VoteFactory(choice=choice_juff, user=member)
        VoteFactory(choice=choice_juff, user=aspirant)
        VoteFactory(choice=choice_tuba, user=retiree)

        gallery = GalleryFactory(
            title="The Book of Blue",
            content="Blue is all around",
            created_by=leader,
            modified_by=aspirant,
        )
        for _ in range(3):
            ImageFactory(gallery=gallery)

        MinutesFactory(
            title="Elronds rådlag",
            content="Sleng han i flammane i domsberget!",
            date=date(3018, 10, 25),
            created_by=leader,
            modified_by=leader,
        )

        NavbarItemFactory(
            text="Julekalender",
            link=reverse("advent_calendar:AdventCalendarList"),
            order=0,
            requires_login=True,
        )
        about_dropdown = NavbarItemFactory(
            text="Om oss",
            order=1,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Om oss",
            link=article_about.get_absolute_url(),
            order=1,
            parent=about_dropdown,
        )
        NavbarItemFactory(
            text="Medlemsliste",
            link=reverse("accounts:MemberList"),
            order=2,
            requires_login=True,
            parent=about_dropdown,
        )
        NavbarItemFactory(
            text="Hendingar",
            link=reverse("events:EventList"),
            order=1.5,
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
            link=reverse("repertoire:RepertoireList"),
            order=2,
            requires_login=True,
            parent=sheetmusic_dropdown,
        )
        NavbarItemFactory(
            text="Foto",
            link=reverse("pictures:GalleryList"),
            order=2.5,
            requires_login=True,
        )
        admin_dropdown = NavbarItemFactory(
            text="Administrasjon",
            order=3,
            type=NavbarItem.Type.DROPDOWN,
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
            parent=admin_dropdown,
        )
        NavbarItemFactory(
            text="Lagertilgjenge",
            link=reverse("storage:StorageAccess"),
            order=5,
            requires_login=True,
            parent=admin_dropdown,
            permissions=["accounts.view_storage_access"],
        )
        other_dropdown = NavbarItemFactory(
            text="Anna",
            order=4,
            type=NavbarItem.Type.DROPDOWN,
        )
        NavbarItemFactory(
            text="Songar",
            link=article_songs.get_absolute_url(),
            order=1,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Sitat",
            link=reverse("quotes:quotes"),
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
            text="Forum",
            link=reverse("forum:ForumList"),
            order=2.6,
            requires_login=True,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Buttonpdfgenerator",
            link=reverse("buttons:ButtonsView"),
            order=3,
            parent=other_dropdown,
        )
        NavbarItemFactory(
            text="Søk",
            link=reverse("search:Search"),
            order=5,
            type=NavbarItem.Type.LINK,
        )
        pause_waltz = ScoreFactory(
            title="Pausevalsen",
            arrangement="Ukjend",
            originally_from="Dei Kraftlause",
            sound_link="http://www.ikke.no/",
        )
        pause_waltz_all = PdfFactory(
            score=pause_waltz,
            file=test_pdf_multipage(
                [
                    "Fløyte",
                    "Klarinett 1",
                    "Klarinett 2",
                    "Saxofon",
                    "Trompet",
                    "Trombone",
                    "Juff",
                    "Tuba",
                    "Eb-Tuba",
                    "Trommesett",
                    "El-piano",
                    "VCO",
                    "Loop station",
                ],
                name="Pausevalsen - Alle stemmer.pdf",
            ),
            filename_original="Pausevalsen - Alle stemmer.pdf",
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_flute,
            from_page=1,
            to_page=1,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=1,
            instrument_type=type_clarinet,
            from_page=2,
            to_page=2,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=2,
            instrument_type=type_clarinet,
            from_page=3,
            to_page=3,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_saxophone,
            from_page=4,
            to_page=4,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_trumpet,
            from_page=5,
            to_page=5,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_trombone,
            from_page=6,
            to_page=6,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_euphonium,
            from_page=7,
            to_page=7,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_tuba,
            from_page=8,
            to_page=8,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_tuba,
            note="Eb",
            from_page=9,
            to_page=9,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_drumset,
            from_page=10,
            to_page=10,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_electric_piano,
            from_page=11,
            to_page=11,
        )
        pause_waltz_vco = PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_vco,
            from_page=12,
            to_page=12,
        )
        PartFactory(
            pdf=pause_waltz_all,
            part_number=None,
            instrument_type=type_loop_station,
            from_page=13,
            to_page=13,
        )
        FavoritePartFactory(user=leader, part=pause_waltz_vco)
        concert_repertoire = RepertoireFactory(name="Konsert")
        RepertoireEntryFactory(repertoire=concert_repertoire, score=pause_waltz)
