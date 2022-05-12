from django import http
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core import exceptions
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.static import serve


class DeleteViewCustom(SuccessMessageMixin, DeleteView):
    """
    Custom `DeleteView` with better defaults:

    - Template set to `common/confirm_delete.html`
    - Default success message
    """

    template_name = "common/confirm_delete.html"

    def get_success_message(self, cleaned_data):
        return self.success_message or f"{self.object} vart fjerna."


class InlineFormsetCreateView(CreateView):
    """
    View for creating a model and multiple related models in the same view,
    with an inline formset.

    Extends `CreateView` and inherits all of its functionality.
    The only difference is that the success response is
    returned from `form_and_formset_valid()` rather than `form_valid()`.

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
    View for updating a model and multiple related models in the same view,
    with an inline formset.

    Extends `UpdateView` and inherits all of its functionality.
    The only difference is that the success response is
    returned from `form_and_formset_valid()` rather than `form_valid()`.

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


class ServeMediaFiles(View):
    """
    A generic view for serving media files.
    The most important child is `ServeAllMediaFiles` in the `serve_media_files` app. The test suite for this view also covers the functionality of that view also covers the functionality of this view.
    However, this view is intended for more custom overriding of `get_file_path` together with e.g. no `LoginRequiredMixin`, if it is desirable that the file is publicly available.
    """

    http_method_names = ["get"]
    file_path = None

    def get_file_path(self):
        if self.file_path is None:
            raise exceptions.ImproperlyConfigured(
                f"`file_path` not specified or `get_file_path(self)` not overridden for {self.__class__.__name__}"
            )
        return self.file_path

    def serve_with_django(self, file_path):
        return serve(self.request, file_path, document_root=settings.MEDIA_ROOT)

    def serve_with_nginx(self, file_path):
        file_name = file_path.split("/")[-1]
        response = HttpResponse(
            # Set content_type explicitly to "" so that Nginx inserts it instead
            content_type="",
            headers={
                "Content-Disposition": f'inline; filename="{file_name}"',
                "X-Accel-Redirect": f"{settings.MEDIA_URL_NGINX}{file_path}",
            },
        )
        return response

    def get(self, request, *args, **kwargs):
        file_path = self.get_file_path()
        if settings.DEBUG:
            return self.serve_with_django(file_path)
        return self.serve_with_nginx(file_path)
