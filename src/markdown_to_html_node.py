from block_to_block_type import BlockType, block_to_block_type
from leafnode import LeafNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from text_to_textnodes import text_to_textnodes


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        # Join lines in the paragraph and normalize whitespace
        lines = [line.strip() for line in block.split("\n")]
        text = " ".join(lines)
        children = text_to_children(text)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        # count how many # characters at the start
        level = 0
        for c in block:
            if c == "#":
                level += 1
            else:
                break
        text = block[level + 1 :]  # skip # and the space
        children = text_to_children(text)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        # Split into lines
        lines = block.split("\n")

        # Find start and end of actual code content
        start_idx = 0
        end_idx = len(lines)

        # Skip opening ```
        if lines[start_idx].strip().startswith("```"):
            start_idx += 1

        # Skip closing ```
        if end_idx > start_idx and lines[end_idx - 1].strip() == "```":
            end_idx -= 1

        # Get the code content lines
        code_lines = lines[start_idx:end_idx]

        # Strip leading whitespace but preserve structure
        if code_lines:
            # Remove common leading whitespace
            stripped_lines = [line.lstrip() for line in code_lines]
            inner = "\n".join(stripped_lines) + "\n"  # Always add trailing newline
        else:
            inner = ""

        return ParentNode("pre", [ParentNode("code", [LeafNode(None, inner)])])

    if block_type == BlockType.QUOTE:
        # remove leading ">" from each line
        lines = [line.lstrip("> ").strip() for line in block.split("\n")]
        text = " ".join(lines)
        children = text_to_children(text)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        items = []
        for line in block.split("\n"):
            item_text = line[2:]  # remove "- "
            items.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in block.split("\n"):
            # remove "1. ", "2. ", etc.
            parts = line.split(". ", 1)
            if len(parts) == 2:
                item_text = parts[1]
                items.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode("ol", items)

    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
