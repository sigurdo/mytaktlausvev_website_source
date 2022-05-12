from django.contrib.auth.mixins import LoginRequiredMixin

from common.views import ServeMediaFiles


class ServeAllMediaFiles(LoginRequiredMixin, ServeMediaFiles):
    def get_file_path(self):
        return self.kwargs["path"]
