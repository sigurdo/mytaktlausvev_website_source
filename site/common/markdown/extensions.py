from marko.inline import InlineElement


class KWordCensor(InlineElement):
    """Censor the dreaded K-word. Censorship can be escaped with `\\`"""

    pattern = r"(\\)?(korps)(?i)"

    def __init__(self, match):
        self.should_censor = match.group(1) != "\\"
        self.word = match.group(2)


class KWordCensorMixin:
    def render_k_word_censor(self, element):
        if not element.should_censor:
            return element.word
        return element.word[0] + "*" * (len(element.word) - 1)


class KWordCensorExtension:
    elements = [KWordCensor]
    renderer_mixins = [KWordCensorMixin]


class HardBreakMixin:
    """
    Alywas render line breaks as hard breaks.

    See the GitHub-Flavored Markdown spec for an explanation:
    https://github.github.com/gfm/#hard-line-breaks
    """

    def render_line_break(self, _) -> str:
        return "<br />\n"


class NewlineToBreakExtension:
    renderer_mixins = [HardBreakMixin]
