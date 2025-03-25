import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_not_eq_type_and_text(self):
        node1 = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a code text node", TextType.CODE_TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.CODE_TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT, url="123")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
