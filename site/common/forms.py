from crispy_forms.layout import TEMPLATE_PACK, LayoutObject
from django.template.loader import render_to_string


class FormsetLayoutObject(LayoutObject):
    """
    Boiled from https://stackoverflow.com/questions/15157262/django-crispy-forms-nesting-a-formset-within-a-form

    A crispy Layout object that renders a formset given by `formset_name_in_context` in the middle of a form.

    This is kind-of a hack, since it requires you insert the formset into the context somewhere else, but hey,
    it works, and it enables you to define and manage the formset in a completely separate class, which is
    a lot more natively supported in django.

    Tip: If you use `common/form.html` you can set `render_formset=False` in the context to not render the formset
    below the form as well.
    """

    template = "common/table_inline_formset_shade_delete.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context

        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {"wrapper": self, "formset": formset})
