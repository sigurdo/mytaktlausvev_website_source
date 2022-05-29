from django import http
from django.contrib.messages.views import SuccessMessageMixin
from django.core import exceptions
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class DeleteViewCustom(SuccessMessageMixin, DeleteView):
    """
    Custom `DeleteView` with better defaults:

    - Template set to `common/forms/confirm_delete.html`
    - Default success message
    """

    template_name = "common/forms/confirm_delete.html"

    def get_success_message(self, cleaned_data):
        return self.success_message or f"{self.object} vart fjerna."


class InlineFormsetCreateView(CreateView):
    """
    View for creating a model and multiple related models in the same view,
    with an inline formset.

    Extends `CreateView` and inherits all of its functionality.
    There are two main differences:
    - The success response is returned from
        `form_and_formset_valid()` rather than `form_valid()`.
    - `form_invalid()` has been replaced by a shared `form_or_formset_invalid()`.

    Formset functionality is almost identical to form functionality.
    The implementor must define `formset_class`.
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

    def form_and_formset_valid(self, form, formset):
        """
        If both the form and the formset is valid,
        redirect to the supplied URL.
        """
        self.form_valid(form)
        self.formset_valid(formset)
        return HttpResponseRedirect(self.get_success_url())

    def form_or_formset_invalid(self, form, formset):
        """
        If either the form or the formset is invalid,
        render the invalid form and/or formset.
        """
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        with transaction.atomic():
            form = self.get_form()
            formset = self.get_formset()
            if form.is_valid() and formset.is_valid():
                return self.form_and_formset_valid(form, formset)

        return self.form_or_formset_invalid(form, formset)


class InlineFormsetUpdateView(UpdateView):
    """
    View for updating a model and multiple related models in the same view,
    with an inline formset.

    Extends `UpdateView` and inherits all of its functionality.
    There are two main differences:
    - The success response is returned from
        `form_and_formset_valid()` rather than `form_valid()`.
    - `form_invalid()` has been replaced by a shared `form_or_formset_invalid()`.

    Formset functionality is almost identical to form functionality.
    The implementor must define `formset_class`.
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

    def form_and_formset_valid(self, form, formset):
        """
        If both the form and the formset is valid,
        redirect to the supplied URL.
        """
        self.form_valid(form)
        self.formset_valid(formset)
        return HttpResponseRedirect(self.get_success_url())

    def form_or_formset_invalid(self, form, formset):
        """
        If either the form or the formset is invalid,
        render the invalid form and/or formset.
        """
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            form = self.get_form()
            formset = self.get_formset()
            if form.is_valid() and formset.is_valid():
                return self.form_and_formset_valid(form, formset)

        return self.form_or_formset_invalid(form, formset)


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
