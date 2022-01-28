from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor, SimpleTagPattern
from markdown.treeprocessors import Treeprocessor


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


class StrikethroughExtension(Extension):
    """
    Adds the possibility to use "~~something~~" to create a span that looks like <del>something</del>
    """

    RE = r"(~~)(.*?)~~"

    def extendMarkdown(self, md):
        del_tag = SimpleTagPattern(self.RE, "del")
        md.inlinePatterns.add("del", del_tag, "_begin")


class UnderlineExtension(Extension):
    """
    Adds the possibility to use "__something__" to create a span that looks like <ins>something</ins>
    """

    RE = r"(__)(.*?)__"

    def extendMarkdown(self, md):
        ins_tag = SimpleTagPattern(self.RE, "ins")
        md.inlinePatterns.add("ins", ins_tag, ">del")


class CensorshipProcessor(InlineProcessor):
    """Censors everything except the first letter of the matched string."""

    def handleMatch(self, m, data):
        censored = m.group(0)[0] + "*" * (len(m.group(0)) - 1)
        return censored, m.start(0), m.end(0)


class KWordCensorExtension(Extension):
    """Markdown extension that censors the dreaded K-word."""

    RE = r"(K|k)orps"

    def extendMarkdown(self, md):
        md.inlinePatterns.register(CensorshipProcessor(self.RE), "k-word-censor", 451)
