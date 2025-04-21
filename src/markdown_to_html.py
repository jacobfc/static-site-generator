from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

from htmlnode import LeafNode, ParentNode


def text_to_children(text):
    list_of_textnodes = text_to_textnodes(text)
    list_of_htmlnodes = []
    for textnode in list_of_textnodes:
        list_of_textnodes.append(text_node_to_html_node(textnode))
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
                print(f"\nblock: {block}")
                # TODO: strip "```" characters from text
                code_block = TextNode(block, TextType.CODE_TEXT)
                print(f"\ncode_block: {code_block}")
                html_code_node = text_node_to_html_node(code_block)
                # add <pre> wrapper (ParentNode) for multi-line code blocks
                html_node_with_pre = ParentNode("pre", [html_code_node])
                blocks_output_list.append(html_node_with_pre)

            case BlockType.PARAGRAPH:
                children_html_nodes = text_to_children(block)
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
                # TODO: remove hashes from heading text?
                # cleaned_block =
                children_html_nodes = text_to_children(block)

                parent_block_node = ParentNode(header_string, children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.QUOTE:
                # TODO: remove "<" from quote lines?
                children_html_nodes = text_to_children(block)
                parent_block_node = ParentNode("blockquote", children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.UNORDERED_LIST:
                children_html_nodes = text_to_children(block)
                # TODO: add wraping of <li> tags, and remove "- " from list items?
                parent_block_node = ParentNode("ul", children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case BlockType.ORDERED_LIST:
                children_html_nodes = text_to_children(block)
                # TODO: add wraping of <li> tags, and remove "X. " from list items?
                parent_block_node = ParentNode("ol", children_html_nodes)
                blocks_output_list.append(parent_block_node)

            case _:
                raise ValueError("No valid BlockType value")

    # TODO: convert blocks_output_list to single parent HTML node (div class?)
    print(f"\nblocks_output_list: {blocks_output_list}")
    html_parent = ParentNode("div", blocks_output_list)
    return html_parent
