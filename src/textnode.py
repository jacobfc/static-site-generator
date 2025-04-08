from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        result = (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        )
        return result

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            leaf_node = LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD_TEXT:
            leaf_node = LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            leaf_node = LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            leaf_node = LeafNode("code", text_node.text)
        case TextType.LINKS:
            assert text_node.url is not None  # require a URL for a link text
            leaf_node = LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGES:
            assert text_node.url is not None  # require a URL for an image link
            leaf_node = LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("No valid TextType value")

    return leaf_node
