from django.views.generic import TemplateView


class PdfReadMinimalMixin:
    template_name = "common/pdfs/pdf_read_minimal.html"

    def pdf_url(self):
        raise NotImplementedError("`pdf_url()` not implemented")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pdf_url"] = self.pdf_url()
        return context


class PdfReadMinimalView(PdfReadMinimalMixin, TemplateView):
    def pdf_url(self):
        return self.request.GET["pdf_url"]
