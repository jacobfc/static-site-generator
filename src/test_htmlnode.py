import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
