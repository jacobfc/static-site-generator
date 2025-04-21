from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "HEADING"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    non_empty_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            non_empty_blocks.append(stripped_block)

    return non_empty_blocks


def block_to_block_type(markdown_block):
    first_character = markdown_block[0]
    # choose which checks to perform, based on first character in block
    match first_character:
        case "#":  # check if block is a  heading
            if block_is_heading(markdown_block):
                return BlockType.HEADING
        case "`":  # check if block is a code block
            if block_is_code(markdown_block):
                return BlockType.CODE
        case ">":  # check if block is a quote block
            if block_is_quote(markdown_block):
                return BlockType.QUOTE
        case "-":  # possible unordered list
            if block_is_unordered_list(markdown_block):
                return BlockType.UNORDERED_LIST
        case "1":  # possible ordered list
            if block_is_ordered_list(markdown_block):
                return BlockType.ORDERED_LIST

        # case _:  # no matches; default back to "normal" paragraph
        #    return BlockType.PARAGRAPH
    return BlockType.PARAGRAPH


def block_is_heading(markdown_block):
    num_leading_hashes = 0
    current_char = markdown_block[num_leading_hashes]
    while current_char == "#":
        num_leading_hashes += 1

        # require that markdown block must have characters afterwards
        assert len(markdown_block) >= num_leading_hashes

        current_char = markdown_block[num_leading_hashes]

    # minimum 1, maximum 6 hashes for heading blocks
    if (1 <= num_leading_hashes) and (num_leading_hashes <= 6):
        # hashes must be followed by a space
        if markdown_block[num_leading_hashes] == " ":
            # space must be followed by text
            # TODO: better check for if title text is valid? (e.g. not just whitespace?)
            if len(markdown_block) > num_leading_hashes + 1:
                return True

    return False


def block_is_code(markdown_block):
    # TODO: check for whether the block doesn't have ``` in the middle?
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return True
    return False


def block_is_quote(markdown_block):
    # split into lines, to check whether they start with ">"
    split_lines = markdown_block.split("\n")
    for line in split_lines:
        if not line.startswith(">"):
            return False

    return True


def block_is_unordered_list(markdown_block):
    # split into lines, to check whether they start with "- "
    split_lines = markdown_block.split("\n")
    for line in split_lines:
        if not line.startswith("- "):
            return False

    return True


def block_is_ordered_list(markdown_block):
    # split into lines, to check whether they start with "X. ", where X is the item number
    split_lines = markdown_block.split("\n")
    item_number = 1  # check whether the number starting in the line is correct
    for line in split_lines:
        string_to_check_start = str(item_number) + ". "
        if not line.startswith(string_to_check_start):
            return False
        item_number += 1

    return True
