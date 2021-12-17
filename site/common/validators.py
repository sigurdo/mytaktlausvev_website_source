import os

from django.utils.deconstruct import deconstructible
from django.forms import ValidationError

import magic


@deconstructible
class FileTypeValidator(object):
    def __init__(self, allowed_types):
        """
        allowed_types should be a dictionary of keys being the allowed file types, and values
        being a list of the allowed file extensions for that file type
        """
        self.allowed_types = allowed_types

    def __call__(self, data):
        extension = os.path.splitext(data.name)[1].lower()
        content_type = magic.from_buffer(data.read(), mime=True)
        data.seek(0)
        if content_type not in self.allowed_types:
            raise ValidationError(f"{data.name}: Filtype {content_type} ikkje lovleg")
        if extension not in self.allowed_types[content_type]:
            raise ValidationError(
                f"{data.name}: Filending {extension} ikkje lovleg for {content_type}"
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileTypeValidator)
            and self.allowed_types == other.allowed_types
        )
