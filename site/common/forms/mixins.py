from django.forms import FileField, ValidationError


class CleanAllFilesMixin:
    """
    Mixin that ensures that all files uploaded
    to a `FileField` are cleaned.

    For some reason, Django only calls field.clean() on the last file, so
    we have to call field.clean() on all others manually.
    """

    def _clean_fields(self):
        super()._clean_fields()
        for name, field in self.fields.items():
            if isinstance(field, FileField):
                for file in self.files.getlist(name)[:-1]:
                    try:
                        field.clean(file)
                    except ValidationError as exception:
                        self.add_error(name, exception)
