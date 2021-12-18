import os.path

from django.core.management.base import BaseCommand
from pygments.formatters import HtmlFormatter


class Command(BaseCommand):
    help = "Generates code styles `styles` by writing to `directory`."

    def add_arguments(self, parser):
        parser.add_argument("directory", type=str)
        parser.add_argument("styles", nargs="+", type=str)

    def _write_style(self, directory, style):
        path = os.path.join(directory, f"codestyle-{style}.scss")
        formatter = HtmlFormatter(cssclass="codehilite", style=style)
        with open(path, "w") as file:
            file.write(formatter.get_style_defs())

    def handle(self, **options):
        directory = options["directory"]
        for style in options["styles"]:
            self._write_style(directory, style)
