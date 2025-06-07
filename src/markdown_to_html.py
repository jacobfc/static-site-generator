from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

from htmlnode import ParentNode


def text_to_children(text):
    list_of_textnodes = text_to_textnodes(text)
    list_of_htmlnodes = []
    for textnode in list_of_textnodes:
        list_of_htmlnodes.append(text_node_to_html_node(textnode))
    return list_of_htmlnodes


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    blocks_output_list = []

    for block in markdown_blocks:
        # block_parent_node = ParentNode()
        block_type = block_to_block_type(block)

        match block_type:
            # special case for code blocks; no inline parsing of children
            case BlockType.CODE:
                # strip "```" from both the beginning and end of the block,
                # and strip whitespace at the beginning of the block with lstrip()
                stripped_block = block.strip("`").lstrip()
                code_block = TextNode(stripped_block, TextType.CODE_TEXT)
                html_code_node = text_node_to_html_node(code_block)
                # add <pre> wrapper (ParentNode) for multi-line code blocks
                html_node_with_pre = ParentNode("pre", [html_code_node])
                blocks_output_list.append(html_node_with_pre)

            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                children_html_nodes = text_to_children(paragraph)
                parent_block_node = ParentNode("p", children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.HEADING:
                # for headings, count number of hashes
                num_leading_hashes = 0
                current_char = block[num_leading_hashes]
                while current_char == "#":
                    num_leading_hashes += 1
                    # require that markdown block must have characters afterwards
                    assert len(block) >= num_leading_hashes
                    current_char = block[num_leading_hashes]

                header_string = "h" + str(num_leading_hashes)
                # remove and space hashes from start of text
                chars_to_remove = num_leading_hashes + 1
                cleaned_block = block[chars_to_remove:]
                children_html_nodes = text_to_children(cleaned_block)
                parent_block_node = ParentNode(header_string, children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    # remove ">" and whitespace from markdown text
                    new_lines.append(line.lstrip(">").strip())

                content = " ".join(new_lines)
                children_html_nodes = text_to_children(content)
                parent_block_node = ParentNode("blockquote", children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[2:]  # remove "- " from list items
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                parent_block_node = ParentNode("ul", html_items)
                blocks_output_list.append(parent_block_node)

            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[3:]  # remove "X. " from list items
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                parent_block_node = ParentNode("ol", html_items)
                blocks_output_list.append(parent_block_node)

            case _:
                raise ValueError("No valid BlockType value")

    html_parent = ParentNode("div", blocks_output_list)
    return html_parent


def extract_title(markdown):
    markdown_lines = markdown.splitlines()
    for line in markdown_lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()

    # if no h1 header:
    raise ValueError("No h1 header in the markdown - no title to extract")
