import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
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


class TestRegexes(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and"
            " [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


class TestImageLinkNodeSplitter(unittest.TestCase):
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGES, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and"
            " another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](boot.dev) and another [second link](en.wikipedia.org)",
            TextType.NORMAL_TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINKS, "boot.dev"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second link", TextType.LINKS, "en.wikipedia.org"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
