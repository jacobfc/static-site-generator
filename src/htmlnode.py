class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        # prevent type issues if props has no value
        if self.props is None:
            return ""

        # convert dict to ` key=value` , with leading space
        prop_html_string = ""
        for item in self.props:
            prop_html_string += " " + item + '="' + self.props[item] + '"'

        return prop_html_string

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, value={self.value},"
            f" children={self.children}, props={self.props})"
        )


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
