from datetime import datetime
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class BootstrapTableProcessor(Treeprocessor):
    """Finds all tables and adds the classes `table table-striped`"""

    def run(self, root):
        tables = root.findall("table")
        for table in tables:
            table.set("class", "table table-striped")


class BootstrapTableExtension(Extension):
    """Add Bootstrap classes `table table-striped` to tables."""

    def extendMarkdown(self, md):
        """Add an instance of `BootstrapTableProcessor` to `Treeprocessor`."""
        md.treeprocessors.register(
            BootstrapTableProcessor(md.parser), "bootstrap-tables", 42
        )
