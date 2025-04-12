def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    non_empty_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            non_empty_blocks.append(stripped_block)

    return non_empty_blocks
