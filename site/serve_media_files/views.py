from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import exceptions
from django.http.response import HttpResponse
from django.views import View
from django.views.static import serve


class ServeMediaFiles(View):
    """
    A generic view for serving media files, intended for inheriting.
    The most important child is `ServeAllMediaFiles`, implemented right below. The test suite for that view also covers the functionality of this view.
    However, this view is also intended for custom overriding of `get_file_path` together with e.g. no `LoginRequiredMixin`, if it is desirable that the file is publicly available.
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
                "X-Accel-Redirect": f'"{settings.MEDIA_URL_NGINX}{file_path}"',
            },
        )
        return response

    def get(self, request, *args, **kwargs):
        file_path = self.get_file_path()
        if settings.DEBUG:
            return self.serve_with_django(file_path)
        return self.serve_with_nginx(file_path)


class ServeAllMediaFiles(LoginRequiredMixin, ServeMediaFiles):
    def get_file_path(self):
        return self.kwargs["path"]
