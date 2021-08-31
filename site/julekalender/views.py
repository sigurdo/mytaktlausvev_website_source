import random
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import Julekalender, Window
from .forms import CalendarForm, WindowForm


class JulekalenderList(ListView):
    """View for viewing all julekalenders."""

    model = Julekalender


class JulekalenderCreate(CreateView):
    """View for creating julekalenders."""

    model = Julekalender
    form_class = CalendarForm


class JulekalenderDetail(DetailView):
    """View for viewing a julekalender."""

    model = Julekalender

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        random.seed(context["julekalender"].year)
        context["permutation"] = random.sample(range(1, 25), 24)
        context["form"] = WindowForm(initial={"calendar": context["julekalender"]})

        return context


class WindowCreate(CreateView):
    """View for viewing a julekalender window."""

    model = Window
    form_class = WindowForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.calendar.get_absolute_url()
