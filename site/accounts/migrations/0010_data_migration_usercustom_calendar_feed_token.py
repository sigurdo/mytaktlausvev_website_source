from django.db import migrations
from secrets import token_urlsafe


def generate_calendar_feed_tokens(apps, schema_editor):
    UserCustom = apps.get_model("accounts", "UserCustom")
    for user in UserCustom.objects.all():
        user.calendar_feed_token = token_urlsafe()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_usercustom_calendar_feed_only_upcoming_and_more"),
    ]

    operations = [
        migrations.RunPython(generate_calendar_feed_tokens),
    ]
