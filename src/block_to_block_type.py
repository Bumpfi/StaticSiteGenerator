from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    # Heading
    if markdown_block.startswith("#"):
        parts = markdown_block.split(" ", 1)
        if len(parts) == 2:
            hashes = parts[0]
            if 1 <= len(hashes) <= 6 and parts[1].strip() != "":
                return BlockType.HEADING

    # CodeBlock
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    lines = markdown_block.split("\n")

    # QuoteBlock
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # UnorderedList
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # OrderedList "1. "
    if all(line.startswith(str(i + 1) + ". ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # if no than paragraph
    return BlockType.PARAGRAPH
