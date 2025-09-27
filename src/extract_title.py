def extract_title(markdown):
    """
    Extract the H1 header from markdown content.

    Args:
        markdown (str): The markdown content to extract the title from

    Returns:
        str: The title text without the # and leading/trailing whitespace

    Raises:
        Exception: If no H1 header is found
    """
    lines = markdown.split("\n")

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# ") and not stripped_line.startswith("## "):
            # Found an H1 header, extract the title
            title = stripped_line[1:].strip()  # Remove the # and any whitespace
            return title
        elif stripped_line == "#":
            # Edge case: just a # with no title
            return ""

    # No H1 header found
    raise Exception("No H1 header found in markdown")
