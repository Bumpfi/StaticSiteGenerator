import os
import shutil

from generate_page import generate_pages_recursive


def copy_static_to_public(src_dir="static", dest_dir="public"):
    """
    Recursively copies all contents from source directory to destination directory.
    First deletes all contents of destination directory for a clean copy.
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create destination directory
    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    # Copy all contents from source to destination
    _copy_directory_contents(src_dir, dest_dir)


def _copy_directory_contents(src_dir, dest_dir):
    """
    Recursively copies contents of src_dir to dest_dir.
    Helper function for copy_static_to_public.
    """
    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {src_dir}")
        return

    # Get all items in source directory
    items = os.listdir(src_dir)

    for item in items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            # It's a file - copy it
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # It's a directory - create it and recursively copy contents
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
            _copy_directory_contents(src_path, dest_path)


def main():
    """
    Main function to run the static site generator.
    """
    print("Starting static site generator...")

    # Delete anything in the public directory
    copy_static_to_public()

    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "public")

    print("Site generation completed successfully!")


if __name__ == "__main__":
    main()
