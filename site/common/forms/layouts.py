from crispy_forms.layout import TEMPLATE_PACK, Button, LayoutObject
from crispy_forms.utils import render_crispy_form


class DynamicFormsetButton(Button):
    """
    Creates a button used to dynamically add more forms to a formset,
    through `common/forms/dynamic_formset.js`.
    The button is styled to set it apart from other components in the form.
    """

    def __init__(self, button_text, **kwargs):
        super().__init__("Add form", button_text, data_formset_add_form=True, **kwargs)
        self.field_classes = "btn btn-secondary d-block mb-3"


class FormsetLayoutObject(LayoutObject):
    """
    Boiled from https://stackoverflow.com/questions/15157262/django-crispy-forms-nesting-a-formset-within-a-form

    A crispy Layout object that renders a formset given by `formset_name_in_context` in the middle of a form.

    This is kind-of a hack, since it requires you insert the formset into the context somewhere else, but hey,
    it works, and it enables you to define and manage the formset in a completely separate class, which is
    a lot more natively supported in django.

    Tip: If you use `common/forms/form.html` you can set `render_formset=False` in the context to not render the formset
    below the form as well.
    """

    def __init__(self, formset_name_in_context="formset", helper=None):
        self.formset_name_in_context = formset_name_in_context
        self.helper = helper

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]

        # `self.helper` should have priority over `formset.helper`
        helper = self.helper
        if helper is None and hasattr(formset, "helper"):
            helper = formset.helper

        # A rendered `LayoutObject` should not contain form tags
        helper.form_tag = False

        return render_crispy_form(
            formset,
            helper=helper,
            context={"wrapper": self, "formset": formset, "form_show_errors": True},
        )
