import multiprocessing

import PIL
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, UpdateView

from buttons.models import ButtonDesign
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .button_pdf_generator import button_pdf_generator
from .forms import ButtonDesignForm, ButtonsForm


def breadcrumbs():
    """Returns breadcrumbs for the button views."""
    breadcrumbs = [Breadcrumb(reverse("buttons:ButtonsView"), "Buttons")]
    return breadcrumbs


class ButtonsView(FormView):
    form_class = ButtonsForm
    template_name = "buttons/buttons_view.html"

    def get_context_data(self, **kwargs):
        button_designs = (
            ButtonDesign.objects.all()
            if self.request.user.is_authenticated
            else ButtonDesign.objects.filter(public=True)
        )
        kwargs["button_designs"] = button_designs
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        images = self.request.FILES.getlist("images")
        if len(images) > 64:
            return HttpResponseBadRequest(
                "Kan ikkje bruke fleire enn 64 ulike motiv samstundes"
            )
        images = [PIL.Image.open(image) for image in images]
        num_of_each = form.cleaned_data["num_of_each"]
        button_visible_diameter_mm = form.cleaned_data["button_visible_diameter_mm"]

        # Perform PDF generation in a multiprocessing pool to retain responsiveness for other
        # requests in the meantime.
        pdf = multiprocessing.Pool().apply(
            button_pdf_generator,
            [images],
            {
                "num_of_each": num_of_each,
                "button_visible_width_mm": button_visible_diameter_mm,
                "button_visible_height_mm": button_visible_diameter_mm,
            },
        )
        return FileResponse(pdf, content_type="application/pdf", filename="buttons.pdf")


class ButtonDesignRedirect(UserPassesTestMixin, RedirectView):
    def setup(self, request, *args, **kwargs):
        self.button_design = ButtonDesign.objects.get(slug=kwargs["slug"])
        super().setup(request, *args, **kwargs)

    def test_func(self):
        if self.button_design.public:
            return True
        return self.request.user.is_authenticated

    def get_redirect_url(self, *args, **kwargs):
        return self.button_design.image.url


class ButtonDesignCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = ButtonDesign
    form_class = ButtonDesignForm
    template_name = "common/forms/form.html"
    success_message = 'Buttonmotivet "%(name)s" vart laga.'
    success_url = reverse_lazy("buttons:ButtonsView")

    def get_breadcrumbs(self):
        return breadcrumbs()


class ButtonDesignUpdate(
    PermissionOrCreatedMixin, SuccessMessageMixin, BreadcrumbsMixin, UpdateView
):
    model = ButtonDesign
    form_class = ButtonDesignForm
    template_name = "common/forms/form.html"
    success_message = 'Buttonmotivet "%(name)s" vart oppdatert.'
    success_url = reverse_lazy("buttons:ButtonsView")
    permission_required = "buttons.change_buttondesign"

    def get_breadcrumbs(self):
        return breadcrumbs()


class ButtonDesignDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = ButtonDesign
    success_url = reverse_lazy("buttons:ButtonsView")
    permission_required = "buttons.delete_buttondesign"

    def get_breadcrumbs(self):
        return breadcrumbs()
