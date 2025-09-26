from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_modes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_modes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax, unbalanced delimiter: {delimiter}"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_modes.append(TextNode(part, TextType.TEXT))
            else:
                new_modes.append(TextNode(part, text_type))

    return new_modes
