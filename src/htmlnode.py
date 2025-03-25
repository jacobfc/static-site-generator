class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
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
