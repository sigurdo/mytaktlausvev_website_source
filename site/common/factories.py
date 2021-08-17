import factory
from django.conf import settings
from django.contrib.auth.models import Permission


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ("username",)

    username = "user"
    password = "password"

    @factory.post_generation
    def permissions(self, create, permission_list):
        if not create or not permission_list:
            return

        for permission in permission_list:
            (app_label, codename) = permission.split(".")
            self.user_permissions.add(
                Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
            )


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = "root"
    password = "password"
    is_staff = True
    is_superuser = True
