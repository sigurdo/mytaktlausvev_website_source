from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.views.generic import FormView, ListView

from accounts.models import UserCustom

from .forms import AddJacketUserForm, JacketsUpdateFormset, RemoveJacketUserForm
from .models import Jacket


class JacketList(LoginRequiredMixin, ListView):
    model = Jacket
    context_object_name = "jackets"


class JacketsUpdate(PermissionRequiredMixin, FormView):
    form_class = JacketsUpdateFormset
    template_name = "common/form.html"
    permission_required = (
        "uniforms.add_jacket",
        "uniforms.change_jacket",
        "uniforms.delete_jacket",
    )

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger jakkeoversikt"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # We must explicitly save form since this a FormView and not an UpdateView
        form.save()
        return super().form_valid(form)


class JacketUsers(PermissionRequiredMixin, ListView):
    model = UserCustom
    context_object_name = "users"
    template_name = "uniforms/jacket_user_list.html"
    # This view does not really need to require any permissions since the actual
    # operations are protected by other views, but it is clean to have it since
    # the user won't find anything useful here at all if it does not have these
    # permsissions
    permission_required = (
        "uniforms.change_jacket",
        "accounts.change_usercustom",
    )

    def get_context_data(self, **kwargs):
        kwargs["jacket"] = self.jacket
        return super().get_context_data(**kwargs)

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return UserCustom.objects.filter(jacket=self.jacket)


class AddJacketUser(PermissionRequiredMixin, FormView):
    form_class = AddJacketUserForm
    template_name = "common/form.html"
    permission_required = (
        "uniforms.change_jacket",
        "accounts.change_usercustom",
    )

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        return super().setup(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Legg til brukar av jakke {self.jacket.number}"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = UserCustom.objects.get(pk=form.cleaned_data["user"])
            user.jacket = self.jacket
            user.save()
            if form.cleaned_data["remove_old_ownerships"]:
                for jacket in Jacket.objects.filter(owner=user):
                    jacket.owner = None
                    jacket.save()
            if form.cleaned_data["set_owner"]:
                self.jacket.owner = user
                self.jacket.save()
        return super().form_valid(form)


class RemoveJacketUser(PermissionRequiredMixin, FormView):
    form_class = RemoveJacketUserForm
    template_name = "common/form.html"
    permission_required = (
        "uniforms.change_jacket",
        "accounts.change_usercustom",
    )

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        self.user = UserCustom.objects.get(slug=kwargs["user_slug"])
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs[
            "form_title"
        ] = f"Fjern {self.user} som brukar av jakke {self.jacket.number}"
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def form_valid(self, form):
        with transaction.atomic():
            self.user.jacket = None
            self.user.save()
            if form.cleaned_data["remove_owner"]:
                if self.jacket.owner == self.user:
                    self.jacket.owner = None
                    self.jacket.save()
        return super().form_valid(form)
