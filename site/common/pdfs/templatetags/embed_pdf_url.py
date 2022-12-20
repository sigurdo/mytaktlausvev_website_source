from django import template
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def embed_pdf_url(pdf_url):
    return mark_safe(f"{static('js/pdf.js/web/viewer.html')}?file={pdf_url}")


@register.filter
def embed_pdf_url_minimal(pdf_url):
    return mark_safe(f"{reverse('pdfs:PdfReadMinimalView')}?pdf_url={pdf_url}")
