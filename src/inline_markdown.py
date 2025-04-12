import re

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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        # find images within text
        list_image_tuples = extract_markdown_images(old_node.text)

        # return any nodes without images, or which are not "NORMAL_TEXT", without further processing
        if (list_image_tuples == []) or (old_node.text_type != TextType.NORMAL_TEXT):
            new_nodes.append(old_node)
            continue  # skip rest of processing for this node

        remaining_text = original_text
        # split the text around the image markdown
        for image_tuple in list_image_tuples:
            image_text, image_link = image_tuple
            split_text = remaining_text.split(f"![{image_text}]({image_link})", 1)

            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")

            # add prior text and image to the list of nodes (if non-empty string)
            if split_text[0] != "":
                prior_text = TextNode(split_text[0], TextType.NORMAL_TEXT)
                new_nodes.append(prior_text)
            image_node = TextNode(image_text, TextType.IMAGES, url=image_link)
            new_nodes.append(image_node)

            # continue splitting the remaining text on any additional images
            # TODO: this approach assumes that the image tuples
            # are sorted in the order of occurance in the original text.
            # If this is not the case, a different approach is required (recursion?)
            remaining_text = split_text[1]

        # after looping through all image occurances in the text,
        # add remaing text to the list of nodes (if non-empty string)
        if remaining_text != "":
            remaining_text_node = TextNode(remaining_text, TextType.NORMAL_TEXT)
            new_nodes.append(remaining_text_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        # find links within text
        list_link_tuples = extract_markdown_links(old_node.text)

        # return any nodes without links, or which are not "NORMAL_TEXT", without further processing
        if (list_link_tuples == []) or (old_node.text_type != TextType.NORMAL_TEXT):
            new_nodes.append(old_node)
            continue  # skip rest of processing for this node

        remaining_text = original_text
        # split the text around the link markdown
        for link_tuple in list_link_tuples:
            link_text, link_url = link_tuple
            split_text = remaining_text.split(f"[{link_text}]({link_url})", 1)

            if len(split_text) != 2:
                raise ValueError("invalid markdown, link section not closed")

            # add prior text and link to the list of nodes (if non-empty string)
            if split_text[0] != "":
                prior_text = TextNode(split_text[0], TextType.NORMAL_TEXT)
                new_nodes.append(prior_text)
            link_node = TextNode(link_text, TextType.LINKS, url=link_url)
            new_nodes.append(link_node)

            # continue splitting the remaining text on any additional links
            # TODO: this approach assumes that the link tuples
            # are sorted in the order of occurance in the original text.
            # If this is not the case, a different approach is required (recursion?)
            remaining_text = split_text[1]

        # after looping through all link occurances in the text,
        # add remaing text to the list of nodes (if non-empty string)
        if remaining_text != "":
            remaining_text_node = TextNode(remaining_text, TextType.NORMAL_TEXT)
            new_nodes.append(remaining_text_node)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
