from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor, SimpleTagPattern


class StrikethroughExtension(Extension):
    """
    Enables using "~~something~~" to strikethrough text with the `del` tag.
    """

    RE = r"(~~)(.*?)~~"

    def extendMarkdown(self, md):
        md.inlinePatterns.register(SimpleTagPattern(self.RE, "del"), "del-pattern", 200)


class UnderlineExtension(Extension):
    """
    Enables using "__something__" to underline text with the `ins` tag.
    """

    RE = r"(__)(.*?)__"

    def extendMarkdown(self, md):
        md.inlinePatterns.register(SimpleTagPattern(self.RE, "ins"), "ins-pattern", 200)


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
