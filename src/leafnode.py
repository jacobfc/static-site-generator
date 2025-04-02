from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        assert value is not None  # LeafNode must have value specified
        super().__init__(tag=tag, value=value, props=props)
        assert self.children is None  # LeafNode explicitly has no children

    def to_html(self):
        if self.value is None:
            raise ValueError("All LeafNodes must have a value")

        if self.tag is None:
            return self.value

        html_full = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_full
