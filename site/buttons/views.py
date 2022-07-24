import multiprocessing

import PIL
from django.http import FileResponse, HttpResponseBadRequest
from django.views.generic import FormView

from .button_pdf_generator import button_pdf_generator
from .forms import ButtonsForm


class ButtonsView(FormView):
    form_class = ButtonsForm
    template_name = "buttons/buttons_view.html"

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
