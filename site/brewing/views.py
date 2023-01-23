from django.views.generic import TemplateView


class BrewView(TemplateView):
    template_name = "brewing/brewing.html"
