from bleach.html5lib_shim import Filter


class ClassApplyFilter(Filter):
    """Filter that applies specified classes to specified tags."""

    def __init__(self, source, class_map):
        """`class_map` must be a dict of the form `{<class_name>: <classes_to_apply>}`."""
        super().__init__(source)
        self.class_map = class_map

    def __iter__(self):
        for token in Filter.__iter__(self):
            if token["type"] in ("StartTag", "EmptyTag"):
                if token["name"] in self.class_map:
                    token["data"][(None, "class")] = self.class_map[token["name"]]
            yield token
