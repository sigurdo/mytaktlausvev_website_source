from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import CommentCreateForm, CommentUpdateForm
from .models import Comment


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "common/forms/form.html"
    http_method_names = ["post", "put"]


class CommentUpdate(PermissionOrCreatedMixin, UpdateView):
    """View for updating a comment."""

    model = Comment
    form_class = CommentUpdateForm
    template_name = "common/forms/form.html"
    permission_required = "comments.change_comment"


class CommentDelete(PermissionOrCreatedMixin, DeleteViewCustom):
    """View for deleting a comment."""

    model = Comment
    success_message = "Kommentaren vart fjerna."
    permission_required = "comments.delete_comment"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()
