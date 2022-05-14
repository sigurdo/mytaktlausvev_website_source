from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor, SimpleTagPattern
from markdown.treeprocessors import Treeprocessor


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
    """
    Censors everything except the first letter of the matched string.
    Censorship can be escaped with `\\`
    """

    def __init__(self, pattern, md=None):
        """
        Match \\ at the beginning of the pattern,
        to enable escaping the censor.
        """
        super().__init__(f"(\\\)?{pattern}", md)

    def handleMatch(self, m, data):
        if m.group(1) == "\\":
            censored = m.group(0)[1:]
        else:
            censored = m.group(0)[0] + "*" * (len(m.group(0)) - 1)
        return censored, m.start(0), m.end(0)


class KWordCensorExtension(Extension):
    """Markdown extension that censors the dreaded K-word."""

    RE = r"korps(?i)"

    def extendMarkdown(self, md):
        md.inlinePatterns.register(CensorshipProcessor(self.RE), "k-word-censor", 451)
