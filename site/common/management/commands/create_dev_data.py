from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from accounts.models import UserCustom
from articles.factories import ArticleFactory
from contact.factories import ContactCategoryFactory
from events.factories import EventAttendanceFactory, EventFactory
from events.models import Attendance
from instruments.factories import (
    InstrumentFactory,
    InstrumentGroupFactory,
    InstrumentLocationFactory,
)
from instruments.models import Instrument
from uniforms.factories import JacketFactory, JacketLocationFactory
from uniforms.models import Jacket


class Command(BaseCommand):
    def handle(self, **options):
        superuser = UserCustom.objects.create_superuser(
            "leiar", "leiar@taktlaus.no", "password"
        )
        aspirant = UserCustom.objects.create_user(
            "aspirant",
            "aspirant@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.ACTIVE,
        )
        member = UserCustom.objects.create_user(
            "medlem",
            "medlem@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.ACTIVE,
        )
        retiree = UserCustom.objects.create_user(
            "pensjonist",
            "pensjonist@taktlaus.no",
            "password",
            membership_status=UserCustom.MembershipStatus.RETIRED,
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
            created_by=superuser,
            modified_by=superuser,
        ).save()
        ArticleFactory(
            title="Kalenderfeed-vegvisar",
            content="Importer kalenderfeeden frå [denne](/hendingar/taktlaushendingar.ics) lenkja i kalender-appen din og sett han opp til å oppdatere seg automatisk.",
            public=True,
            comments_allowed=False,
            created_by=superuser,
            modified_by=superuser,
        )

        ContactCategoryFactory(name="Generelt").save()
        ContactCategoryFactory(name="Bli med!").save()

        event = EventFactory(
            title="SMASH",
            content="SMASH in Trondheim",
            created_by=superuser,
            modified_by=superuser,
            start_time=make_aware(datetime.now() + timedelta(365)),
        )
        event.save()
        EventAttendanceFactory(
            event=event, person=superuser, status=Attendance.ATTENDING
        )
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
            created_by=superuser,
            modified_by=superuser,
            start_time=make_aware(first_wednesday),
        )
        EventFactory(
            title="Brettspelkveld",
            content="Brettspelkveld i KJL4.",
            created_by=superuser,
            modified_by=superuser,
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
            created_by=superuser,
            modified_by=superuser,
            start_time=make_aware(datetime_theme_party),
        )
        medal_galla_datetime = datetime(year - 1 if month < 8 else year, 11, 1, 18)
        while medal_galla_datetime.weekday() != 5:
            medal_galla_datetime += timedelta(days=1)
        EventFactory(
            title="Medaljegalla",
            content="Ete lasagne, drikke ulike drikkar og danse.",
            created_by=superuser,
            modified_by=superuser,
            start_time=make_aware(medal_galla_datetime),
        )
        flute = InstrumentGroupFactory(name="Fløyte")
        InstrumentGroupFactory(name="Klarinett")
        trumpet = InstrumentGroupFactory(name="Trompet")
        InstrumentGroupFactory(name="Saxofon")
        InstrumentGroupFactory(name="Trombone")
        InstrumentGroupFactory(name="Juff")
        tuba = InstrumentGroupFactory(name="Tuba")
        main_storage = InstrumentLocationFactory(name="Hovedskapet")
        InstrumentLocationFactory(name="Styreskapet")
        InstrumentLocationFactory(name="Saunaen")
        InstrumentLocationFactory(name="Tatt med hjem")
        member.instrument_group = flute
        member.save()
        InstrumentFactory(
            name="Piccolo 1", group=flute, user=member, location=main_storage
        )
        superuser.instrument_group = trumpet
        superuser.save()
        InstrumentFactory(
            name="Piccolotrompet", group=trumpet, user=superuser, location=main_storage
        )
        InstrumentFactory(
            name="Tuba 2",
            group=tuba,
            location=main_storage,
            comment="Valset over på SMASH",
            state=Instrument.State.UNPLAYABLE,
        )
        jacket_at_home = JacketLocationFactory(
            name="Hjemme",
        )
        jacket_at_storage = JacketLocationFactory(
            name="Jakkeskapet",
        )
        JacketFactory(
            number=1,
            comment="",
            state=Jacket.State.BAD,
            owner=aspirant,
            location=jacket_at_storage,
        )
        JacketFactory(
            number=2,
            comment="Mangler 3 knapper og en lomme",
            state=Jacket.State.UNUSABLE,
            location=jacket_at_storage,
        )
        JacketFactory(
            number=42,
            state=Jacket.State.GOOD,
            owner=superuser,
            location=jacket_at_home,
        )
        JacketFactory(
            number=65,
            state=Jacket.State.OK,
            location=jacket_at_storage,
        )
