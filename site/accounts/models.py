from django.contrib.auth.models import AbstractUser, UserManager
from autoslug import AutoSlugField
from django.urls import reverse


class UserManagerCustom(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if self.filter(username__iexact=username).exists():
            raise ValueError("A user with that username already exists.")
        return super()._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class UserCustom(AbstractUser):
    slug = AutoSlugField(verbose_name="slug", populate_from="username", unique=True)

    objects = UserManagerCustom()

    def get_name(self):
        """Returns the full name if it exists, else the username."""
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("profile", args=[self.slug])
