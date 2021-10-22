from typing import Any, Dict

from django.views.generic.edit import UpdateView
from django import http
from django.core import exceptions


class FormAndFormsetUpdateView(UpdateView):
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
   
    - To make formset elements that are to be deleted gray, and fix a weird bug in crispy forms,
      also add these 2 snippets:
      {% block js %}
          {% load static %}
          <script src="{% static 'common/js/FormAndFormsetUpdateView.js' %}"></script>
      {% endblock js %}
   
      {% block css %}
          {% load sass_tags %}
          <link href="{% sass_src 'common/scss/FormAndFormsetUpdateView.scss' %}" rel="stylesheet" type="text/css">
      {% endblock css %}
    """

    def formset_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))

    def form_valid(self, form: Any) -> responses.HttpResponse:
        formset = self.get_formset()
        if formset.is_valid():
            formset.save()
        else:
            return self.formset_invalid(formset)
        return super().form_valid(form)

    def get_formset_class(self):
        return self.formset_class

    def get_formset_kwargs(self):
        kwargs = {"instance": self.get_object()}
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_formset(self, formset_class=None):
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset()
        if "formset_helper" not in kwargs:
            kwargs["formset_helper"] = self.formset_helper
        return super().get_context_data(**kwargs)

class DeleteMixin():
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
            raise exceptions.ImproperlyConfigured("No URL to redirect to. Provide a delete_success_url.")
        return str(self.delete_success_url)

    def post(self, request, *args, **kwargs):
        if request.POST.get("delete"):
            self.get_object().delete()
            return http.HttpResponseRedirect(self.get_delete_success_url())
        return super().post(request, *args, **kwargs)
