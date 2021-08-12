from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentCreateForm, CommentUpdateForm


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "common/form.html"
    http_method_names = ["post", "put"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    """View for updating a comment."""

    model = Comment
    form_class = CommentUpdateForm
    template_name = "common/form.html"


class CommentDelete(LoginRequiredMixin, DeleteView):
    """View for deleting a comment."""

    model = Comment
    template_name = "common/confirm_delete.html"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()
