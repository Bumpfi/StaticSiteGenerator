import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate a page from markdown content using a template.

    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML should be written
        basepath (str): Base path for URLs (default: "/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Replace absolute URLs with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Write the final HTML to file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    """
    Recursively generate pages from all markdown files in a directory tree.

    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML files
        basepath (str): Base path for URLs (default: "/")
    """
    # Get all items in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        if os.path.isfile(item_path):
            # It's a file - check if it's a markdown file
            if item_path.endswith(".md"):
                # Generate the corresponding HTML file path
                # Replace .md with .html and map to destination directory
                relative_path = os.path.relpath(item_path, dir_path_content)
                html_filename = relative_path.replace(".md", ".html")
                dest_file_path = os.path.join(dest_dir_path, html_filename)

                # Generate the page
                generate_page(item_path, template_path, dest_file_path, basepath)

        elif os.path.isdir(item_path):
            # It's a directory - recursively process it
            # Create corresponding directory in destination
            relative_dir = os.path.relpath(item_path, dir_path_content)
            dest_subdir = os.path.join(dest_dir_path, relative_dir)

            # Recursively process the subdirectory
            generate_pages_recursive(item_path, template_path, dest_subdir, basepath)
