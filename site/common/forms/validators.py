import os

from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileTypeValidator(object):
    def __init__(self, allowed_extensions):
        """`allowed_extensions` should be a list of allowed file extensions."""
        self.allowed_extensions = allowed_extensions

    def __call__(self, data):
        extension = os.path.splitext(data.name)[1].lower()
        if extension not in self.allowed_extensions:
            raise ValidationError(f"{data.name}: Filending '{extension}' ikkje lovleg.")

    def __eq__(self, other):
        return (
            isinstance(other, FileTypeValidator)
            and self.allowed_extensions == other.allowed_extensions
        )
