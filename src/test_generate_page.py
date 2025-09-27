import os
import shutil
import tempfile
import unittest

from generate_page import generate_page


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        """Set up temporary directories for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = os.path.join(self.test_dir, "content")
        self.public_dir = os.path.join(self.test_dir, "public")
        os.makedirs(self.content_dir)
        os.makedirs(self.public_dir)

    def tearDown(self):
        """Clean up temporary directories"""
        shutil.rmtree(self.test_dir)

    def test_generate_page_basic(self):
        """Test basic page generation"""
        # Create test markdown file
        markdown_content = """# Test Title

This is a test paragraph with **bold** text.

## Subheading

- List item 1
- List item 2"""

        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        # Create test template
        template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ Title }}</title>
</head>
<body>
    {{ Content }}
</body>
</html>"""

        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate page
        output_path = os.path.join(self.public_dir, "test.html")
        generate_page(markdown_path, template_path, output_path)

        # Verify output file exists
        self.assertTrue(os.path.exists(output_path))

        # Read and verify content
        with open(output_path, "r") as f:
            result = f.read()

        # Check that title was replaced
        self.assertIn("<title>Test Title</title>", result)

        # Check that content was converted to HTML
        self.assertIn("<h1>Test Title</h1>", result)
        self.assertIn("<b>bold</b>", result)
        self.assertIn("<h2>Subheading</h2>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<li>List item 1</li>", result)

    def test_generate_page_creates_directories(self):
        """Test that generate_page creates necessary directories"""
        # Create test files
        markdown_content = "# Test\nContent here."
        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        template_content = "<html>{{ Title }} - {{ Content }}</html>"
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Output to nested directory that doesn't exist
        nested_dir = os.path.join(self.public_dir, "blog", "posts")
        output_path = os.path.join(nested_dir, "test.html")

        # Directory shouldn't exist before generation
        self.assertFalse(os.path.exists(nested_dir))

        # Generate page
        generate_page(markdown_path, template_path, output_path)

        # Directory should be created and file should exist
        self.assertTrue(os.path.exists(nested_dir))
        self.assertTrue(os.path.exists(output_path))

    def test_generate_page_complex_title(self):
        """Test page generation with complex title"""
        markdown_content = """# The Lord of the Rings: A Journey Through Middle-earth!

Some content here."""

        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        template_content = "<title>{{ Title }}</title><body>{{ Content }}</body>"
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        output_path = os.path.join(self.public_dir, "test.html")
        generate_page(markdown_path, template_path, output_path)

        with open(output_path, "r") as f:
            result = f.read()

        expected_title = "The Lord of the Rings: A Journey Through Middle-earth!"
        self.assertIn(f"<title>{expected_title}</title>", result)

    def test_generate_page_no_h1_raises_exception(self):
        """Test that missing H1 header raises exception during page generation"""
        markdown_content = """## Only H2 headers
Some content without H1."""

        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        template_content = "<title>{{ Title }}</title>"
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        output_path = os.path.join(self.public_dir, "test.html")

        with self.assertRaises(Exception):
            generate_page(markdown_path, template_path, output_path)

    def test_generate_page_multiple_placeholders(self):
        """Test template with multiple instances of same placeholder"""
        markdown_content = "# My Title\nSome content."

        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        template_content = """<title>{{ Title }}</title>
<h1>{{ Title }}</h1>
<div>{{ Content }}</div>
<footer>{{ Title }}</footer>"""

        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        output_path = os.path.join(self.public_dir, "test.html")
        generate_page(markdown_path, template_path, output_path)

        with open(output_path, "r") as f:
            result = f.read()

        # All instances should be replaced
        self.assertIn("<title>My Title</title>", result)
        self.assertIn("<h1>My Title</h1>", result)
        self.assertIn("<footer>My Title</footer>", result)
        self.assertNotIn("{{ Title }}", result)
        self.assertNotIn("{{ Content }}", result)


if __name__ == "__main__":
    unittest.main()
