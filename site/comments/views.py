from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import CreateView
from .models import Comment
from .forms import CommentForm


class CommentCreate(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "common/form.html"
    http_method_names = ["post", "put"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
