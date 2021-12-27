from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.views.generic import FormView, ListView, View
from django.http import HttpResponseRedirect

from accounts.models import UserCustom

from .forms import AddJacketUserForm, JacketsUpdateFormset, RemoveJacketUserForm
from .models import Jacket, JacketUser


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
    context_object_name = "jacket_users"
    template_name = "uniforms/jacket_user_list.html"
    # This view does not really need to require any permissions since the actual
    # operations are protected by other views, but it is clean to have it since
    # the user won't find anything useful here at all if it does not have these
    # permsissions
    permission_required = (
        "uniforms.add_jacketuser",
        "uniforms.change_jacketuser",
        "uniforms.delete_jacketuser",
    )

    def get_context_data(self, **kwargs):
        kwargs["jacket"] = self.jacket
        return super().get_context_data(**kwargs)

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return JacketUser.objects.filter(jacket=self.jacket)


class AddJacketUser(PermissionRequiredMixin, FormView):
    form_class = AddJacketUserForm
    template_name = "common/form.html"
    permission_required = "uniforms.add_jacketuser"

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        return super().setup(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Legg til brukar av jakke {self.jacket.number}"
        return super().get_context_data(**kwargs)

    def get_form(self):
        """Manually inject jacket into the form for valdation."""
        form = super().get_form()
        form.jacket = self.jacket
        return form

    def form_valid(self, form):
        """Create jacket user."""
        with transaction.atomic():
            user = UserCustom.objects.get(pk=form.cleaned_data["user"])
            set_owner = form.cleaned_data["set_owner"]
            JacketUser(user=user, jacket=self.jacket, is_owner=set_owner).save()
        return super().form_valid(form)


class RemoveJacketUser(PermissionRequiredMixin, FormView):
    form_class = RemoveJacketUserForm
    template_name = "common/form.html"
    permission_required = "uniforms.delete_jacketuser"

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        self.user = UserCustom.objects.get(slug=kwargs["user_slug"])
        self.jacket_user = JacketUser.objects.get(jacket=self.jacket, user=self.user)
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs[
            "form_title"
        ] = f"Fjern {self.user} som brukar av jakke {self.jacket.number}"
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def form_valid(self, form):
        """Delete self.jacket_user and find new owner if transfer_ownership=True."""
        with transaction.atomic():
            self.jacket_user.delete()
            transfer_ownership = form.cleaned_data["transfer_ownership"]
            if transfer_ownership and self.jacket_user.is_owner:
                new_owner = JacketUser.objects.filter(jacket=self.jacket).first()
                if new_owner:
                    new_owner.is_owner = True
                    new_owner.save()
        return super().form_valid(form)


class JacketUserMakeOwner(PermissionRequiredMixin, View):
    http_method_names = ["post"]
    permission_required = "uniforms.change_jacketuser"

    def get_succes_url(self):
        return reverse("uniforms:JacketUsers", args=[self.jacket.number])

    def setup(self, request, *args, **kwargs):
        self.jacket = Jacket.objects.get(number=kwargs["jacket_number"])
        self.user = UserCustom.objects.get(slug=kwargs["user_slug"])
        self.jacket_user = JacketUser.objects.get(jacket=self.jacket, user=self.user)
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Remove all old ownerships on self.jacket and make self.user owner instead."""
        with transaction.atomic():
            for jacket_user in self.jacket.jacket_users.filter(is_owner=True):
                jacket_user.is_owner = False
                jacket_user.save()
            self.jacket_user.is_owner = True
            self.jacket_user.save()
        return HttpResponseRedirect(self.get_succes_url())
