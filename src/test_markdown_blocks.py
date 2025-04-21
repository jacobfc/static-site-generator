import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_1hash(self):
        md_block = """# Title example
followed by lots of text
in the paragraph that follows"""
        expected_result = BlockType.HEADING
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_heading_6hash(self):
        md_block = "###### heading with 6 hashes"
        expected_result = BlockType.HEADING
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_heading_10hash_invalid(self):
        md_block = """########## invalid heading with 10 hashes
text comes afterwards too """
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_code_block(self):
        md_block = """``` example of code
        which is spread
        across mulitple lines```"""
        expected_result = BlockType.CODE
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_code_block_no_ending_invalid(self):
        md_block = """``` example of code,
but with no ending
it just keeps going"""
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_quote_block(self):
        md_block = """> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood."""
        expected_result = BlockType.QUOTE
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_unordered_list(self):
        md_block = """- items in a list
- not any particular order
- across multiple lines
- spaces after the bullet """
        expected_result = BlockType.UNORDERED_LIST
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_ordered_list_valid(self):
        md_block = """1. ordered list
2. everything is ordered starting from 1
3. no gaps, spaces are in order"""
        expected_result = BlockType.ORDERED_LIST
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_ordered_list_invalid_numbers(self):
        md_block = """1. This is a failed ordered list
3. We jump over a few numbers
2. They exist, but not in the right order
5. Or sometimes, we forget that 4 exists"""
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_paragraph_no_matching_start_character(self):
        md_block = """Just a plain ol' paragraph
No fancy characters for me, no sir.
It ain't much, but it's honest work."""
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(expected_result, block_to_block_type(md_block))

    def test_block_to_block_types_from_bootdev(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
