import multiprocessing

import PIL
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, View

from buttons.models import ButtonDesign
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .button_pdf_generator import button_pdf_generator
from .forms import ButtonDesignForm, ButtonsForm


class ButtonsView(BreadcrumbsMixin, FormView):
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
        button_backside_padding_mm = form.cleaned_data["button_backside_padding_mm"]
        button_minimum_distance_mm = form.cleaned_data["button_minimum_distance_mm"]
        paper_margin_mm = form.cleaned_data["paper_margin_mm"]

        # Perform PDF generation in a multiprocessing pool to retain responsiveness for other
        # requests in the meantime.
        pdf = multiprocessing.Pool().apply(
            button_pdf_generator,
            [images],
            {
                "num_of_each": num_of_each,
                "button_visible_width_mm": button_visible_diameter_mm,
                "button_visible_height_mm": button_visible_diameter_mm,
                "button_backside_padding_mm": button_backside_padding_mm,
                "button_minimum_distance_mm": button_minimum_distance_mm,
                "page_margin_top_mm": paper_margin_mm,
                "page_margin_right_mm": paper_margin_mm,
                "page_margin_bottom_mm": paper_margin_mm,
                "page_margin_left_mm": paper_margin_mm,
            },
        )
        return FileResponse(pdf, content_type="application/pdf", filename="buttons.pdf")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(
            url=reverse("buttons:ButtonsView"),
            label="Buttons",
        )


class ButtonDesignServe(UserPassesTestMixin, View):
    def setup(self, request, *args, **kwargs):
        self.button_design = ButtonDesign.objects.get(slug=kwargs["slug"])
        super().setup(request, *args, **kwargs)

    def test_func(self):
        if self.button_design.public:
            return True
        return self.request.user.is_authenticated

    def get(self, *args, **kwargs):
        return FileResponse(
            self.button_design.image.open(), filename=self.button_design.image.name
        )


class ButtonDesignCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = ButtonDesign
    form_class = ButtonDesignForm
    template_name = "common/forms/form.html"
    success_message = 'Buttonmotivet "%(name)s" vart laga.'
    success_url = reverse_lazy("buttons:ButtonsView")
    breadcrumb_parent = ButtonsView


class ButtonDesignUpdate(
    PermissionOrCreatedMixin, SuccessMessageMixin, BreadcrumbsMixin, UpdateView
):
    model = ButtonDesign
    form_class = ButtonDesignForm
    template_name = "common/forms/form.html"
    success_message = 'Buttonmotivet "%(name)s" vart oppdatert.'
    success_url = reverse_lazy("buttons:ButtonsView")
    permission_required = "buttons.change_buttondesign"
    breadcrumb_parent = ButtonsView


class ButtonDesignDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = ButtonDesign
    success_url = reverse_lazy("buttons:ButtonsView")
    permission_required = "buttons.delete_buttondesign"
    breadcrumb_parent = ButtonsView
