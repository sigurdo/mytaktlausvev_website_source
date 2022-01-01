from django import http
from django.core import exceptions
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView


class InlineFormsetCreateView(CreateView):
    """
    View for creating a model and multiple related models with an inline formset.

    Inherits methods and attributes from `CreateView`
    Implementors must also define the `formset_class` attribute.
    """

    def get_context_data(self, **kwargs):
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset()
        return super().get_context_data(**kwargs)

    def get_formset_class(self):
        """Return the formset class to use in the view."""
        return self.formset_class

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the formset."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_formset(self, formset_class=None):
        """Return an instance of the formset to be used in this view."""
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def formset_valid(self, formset):
        """If the formset is valid, save the associated models."""
        formset.instance = self.object
        formset.save()

    def formset_invalid(self, formset):
        """If the formset is invalid, render the invalid formset."""
        return self.render_to_response(self.get_context_data(formset=formset))

    def form_and_formset_valid(self):
        """
        If both the form and the formset is valid,
        redirect to the supplied URL
        """
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = None
        with transaction.atomic():
            form = self.get_form()
            if form.is_valid():
                self.form_valid(form)
            else:
                return self.form_invalid(form)

            formset = self.get_formset()
            if formset.is_valid():
                self.formset_valid(formset)
            else:
                transaction.set_rollback(True)
                return self.formset_invalid(formset)

        return self.form_and_formset_valid()


class InlineFormsetUpdateView(UpdateView):
    """
    Generic example:
    Practical view when you have an instance a of a model A with multiple related instances of a model B,
    and you want to edit both a and a's B instances in one single view. This view therefore has
    bot a form for a and a formset for all it's B's.

    How to use:
    - Write a form class for A called AUpdateForm
    - Write a form class for the subform of the formset for the B's of A called BUpdateForm
    - Make a formset based on this form class using inlineformset_factory called BUpdateFormset
    - Write a form helper for the BUpdateFormset called BUpdateFormsetHelper
      - The template of this helper should be common/table_inline_formset_shade_delete.html
        to improve the UX and fix a weird bug.

    - Define the following attributes on the view class:
    - model = A
    - form_class = AUpdateForm
    - formset_class = BUpdateFormset
    - formset_helper = BUpdateFormsetHelper
    - template_name_suffix = "_update_form"

    - Override the following methods:
    - get_success_url - will typically return reverse("name of view in urls.py", kwargs={...})

    - Write a template called A_update_form.html, and insert this little snippet to insert the form:
      {% load crispy_forms_tags %}
      <form method="post">
          {% crispy form %}
          {% crispy formset formset_helper %}
      </form>
    """

    def get_context_data(self, **kwargs):
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset()
        return super().get_context_data(**kwargs)

    def get_formset_class(self):
        """Return the formset class to use in the view."""
        return self.formset_class

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the formset."""
        kwargs = {}
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_formset(self, formset_class=None):
        """Return an instance of the formset to be used in this view."""
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def formset_valid(self, formset):
        """If the formset is valid, save the associated models."""
        formset.instance = self.object
        formset.save()

    def formset_invalid(self, formset):
        """If the formset is invalid, render the invalid formset."""
        return self.render_to_response(self.get_context_data(formset=formset))

    def form_and_formset_valid(self):
        """
        If both the form and the formset is valid,
        redirect to the supplied URL
        """
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            form = self.get_form()
            if form.is_valid():
                self.form_valid(form)
            else:
                return self.form_invalid(form)

            formset = self.get_formset()
            if formset.is_valid():
                self.formset_valid(formset)
            else:
                transaction.set_rollback(True)
                return self.formset_invalid(formset)

        return self.form_and_formset_valid()


class DeleteMixin:
    """
    How to use:
    - Add this class to the parent classes of your UpdateView or FormAndFormsetUpdateView, or possibly other compatible classes
    - Add a delete button to your form helper, typically like this
      helper.add_input(Submit("delete", "Slett", css_class="btn-danger"))
    - Configure the delete_success_url attribute on the view
    """

    delete_success_url = None

    def get_delete_success_url(self):
        if not self.delete_success_url:
            raise exceptions.ImproperlyConfigured(
                "No URL to redirect to. Provide a delete_success_url."
            )
        return str(self.delete_success_url)

    def post(self, request, *args, **kwargs):
        if request.POST.get("delete"):
            self.get_object().delete()
            return http.HttpResponseRedirect(self.get_delete_success_url())
        return super().post(request, *args, **kwargs)
