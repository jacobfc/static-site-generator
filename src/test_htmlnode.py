import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        props_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_result = ' href="https://www.google.com" target="_blank"'
        actual_result = HTMLNode(props=props_dict).props_to_html()
        self.assertEqual(expected_result, actual_result)

    def test_props_to_html_2(self):
        props_dict = {
            "title": "Wikipedia page for the HTML language",
            "target": "https://en.m.wikipedia.org/wiki/HTML",
        }
        expected_result = (
            ' title="Wikipedia page for the HTML language"'
            ' target="https://en.m.wikipedia.org/wiki/HTML"'
        )
        actual_result = HTMLNode(props=props_dict).props_to_html()
        self.assertEqual(expected_result, actual_result)

    def test_blank_html_repr(self):
        expected_result = "HTMLNode(tag=None, value=None, children=None, props=None)"
        actual_result = str(HTMLNode())
        self.assertEqual(expected_result, actual_result)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=p, value=What a strange world, children=None, props={'class': 'primary'})",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_li(self):
        node = LeafNode("li", "Hello, world!")
        self.assertEqual(node.to_html(), "<li>Hello, world!</li>")

    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", "Hello, world!")
        self.assertEqual(node.to_html(), "<blockquote>Hello, world!</blockquote>")

    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "Hello, world!")
        self.assertEqual(node.to_html(), "<h2>Hello, world!</h2>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
