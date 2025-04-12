from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # return any nodes which are not "NORMAL_TEXT", without further processing
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue  # skip rest of processing for this node

        # split text by delimiter
        split_node = old_node.text.split(delimiter)

        # even number of substrings == non-closed delimiter
        if len(split_node) % 2 == 0:
            raise Exception(
                f"No matching closing delimiter found, for \
                    \ndelimiter: {delimiter} \
                    \nin text: {old_node.text}"
            )

        # create new nodes for each substring
        for i in range(len(split_node)):
            text = split_node[i]

            # skip adding a node for any empty strings
            if text == "":
                continue

            # indexes which are uneven == enclosed by delimiters
            if (i % 2) == 1:
                new_node = TextNode(text, text_type)
            # indexes which are even == regular text (outside the delimiters)
            else:
                new_node = TextNode(text, TextType.NORMAL_TEXT)

            new_nodes.append(new_node)

    return new_nodes
