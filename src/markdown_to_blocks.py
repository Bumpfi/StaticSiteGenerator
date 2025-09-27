def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")

    blocks = []

    for block in raw_blocks:
        clean = block.strip()

        if clean:
            blocks.append(clean)

    return blocks
