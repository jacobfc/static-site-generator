import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_bold_single_phrase(self):
        input_text = "This is text with a **bolded phrase** in the middle"
        input = [TextNode(input_text, TextType.NORMAL_TEXT)]
        expected_output = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("bolded phrase", TextType.BOLD_TEXT),
            TextNode(" in the middle", TextType.NORMAL_TEXT),
        ]
        actual_output = split_nodes_delimiter(input, "**", TextType.BOLD_TEXT)
        self.assertEqual(expected_output, actual_output)

    def test_code_block_start_of_text(self):
        input_text = "`code block` at start with other text"
        input = [TextNode(input_text, TextType.NORMAL_TEXT)]
        expected_output = [
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" at start with other text", TextType.NORMAL_TEXT),
        ]
        actual_output = split_nodes_delimiter(input, "`", TextType.CODE_TEXT)
        self.assertEqual(expected_output, actual_output)

    def test_wrong_delimiter(self):
        input_text = "This is text with a **bolded phrase** in the middle"
        input = [TextNode(input_text, TextType.NORMAL_TEXT)]
        expected_output = [TextNode(input_text, TextType.NORMAL_TEXT)]
        actual_output = split_nodes_delimiter(input, "`", TextType.CODE_TEXT)
        self.assertEqual(expected_output, actual_output)

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded word", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
