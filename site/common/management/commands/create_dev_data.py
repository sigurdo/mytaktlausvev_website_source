from datetime import datetime, timedelta

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
