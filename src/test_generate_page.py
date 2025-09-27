import os
import shutil
import tempfile
import unittest

from generate_page import generate_page, generate_pages_recursive


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


class TestGeneratePagesRecursive(unittest.TestCase):
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

    def test_generate_pages_recursive_single_file(self):
        """Test recursive generation with a single markdown file"""
        # Create test markdown file
        markdown_content = "# Test Page\n\nThis is a test."
        markdown_path = os.path.join(self.content_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        # Create template
        template_content = (
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate pages recursively
        generate_pages_recursive(self.content_dir, template_path, self.public_dir)

        # Verify output file exists
        output_path = os.path.join(self.public_dir, "test.html")
        self.assertTrue(os.path.exists(output_path))

        # Verify content
        with open(output_path, "r") as f:
            result = f.read()
        self.assertIn("<title>Test Page</title>", result)
        self.assertIn("<h1>Test Page</h1>", result)

    def test_generate_pages_recursive_nested_directories(self):
        """Test recursive generation with nested directory structure"""
        # Create nested directory structure
        blog_dir = os.path.join(self.content_dir, "blog")
        post1_dir = os.path.join(blog_dir, "post1")
        post2_dir = os.path.join(blog_dir, "post2")
        os.makedirs(post1_dir)
        os.makedirs(post2_dir)

        # Create markdown files
        files_content = {
            "index.md": "# Home Page\n\nWelcome home!",
            "blog/post1/index.md": "# First Post\n\nThis is the first post.",
            "blog/post2/index.md": "# Second Post\n\nThis is the second post.",
        }

        for rel_path, content in files_content.items():
            full_path = os.path.join(self.content_dir, rel_path)
            with open(full_path, "w") as f:
                f.write(content)

        # Create template
        template_content = (
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate pages recursively
        generate_pages_recursive(self.content_dir, template_path, self.public_dir)

        # Verify all files were generated
        expected_files = [
            "index.html",
            "blog/post1/index.html",
            "blog/post2/index.html",
        ]

        for expected_file in expected_files:
            full_path = os.path.join(self.public_dir, expected_file)
            self.assertTrue(
                os.path.exists(full_path), f"File {expected_file} should exist"
            )

        # Verify content of one nested file
        post1_path = os.path.join(self.public_dir, "blog", "post1", "index.html")
        with open(post1_path, "r") as f:
            result = f.read()
        self.assertIn("<title>First Post</title>", result)
        self.assertIn("<h1>First Post</h1>", result)

    def test_generate_pages_recursive_mixed_files(self):
        """Test recursive generation ignores non-markdown files"""
        # Create mixed file types
        files = {
            "page.md": "# Valid Page\n\nThis should be converted.",
            "readme.txt": "This is a text file.",
            "image.png": b"fake image data",
            "config.json": '{"setting": "value"}',
            "another.md": "# Another Page\n\nAnother valid page.",
        }

        for filename, content in files.items():
            file_path = os.path.join(self.content_dir, filename)
            if isinstance(content, str):
                with open(file_path, "w") as f:
                    f.write(content)
            else:
                with open(file_path, "wb") as f:
                    f.write(content)

        # Create template
        template_content = (
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate pages recursively
        generate_pages_recursive(self.content_dir, template_path, self.public_dir)

        # Only .md files should be converted to .html
        self.assertTrue(os.path.exists(os.path.join(self.public_dir, "page.html")))
        self.assertTrue(os.path.exists(os.path.join(self.public_dir, "another.html")))

        # Non-markdown files should not be converted
        self.assertFalse(os.path.exists(os.path.join(self.public_dir, "readme.html")))
        self.assertFalse(os.path.exists(os.path.join(self.public_dir, "image.html")))
        self.assertFalse(os.path.exists(os.path.join(self.public_dir, "config.html")))

    def test_generate_pages_recursive_empty_directory(self):
        """Test recursive generation with empty directory"""
        # Create template
        template_content = (
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate pages recursively on empty directory
        generate_pages_recursive(self.content_dir, template_path, self.public_dir)

        # Public directory should be empty (except possibly existing structure)
        # No HTML files should be created
        html_files = []
        for root, dirs, files in os.walk(self.public_dir):
            for file in files:
                if file.endswith(".html"):
                    html_files.append(file)
        self.assertEqual(len(html_files), 0)

    def test_generate_pages_recursive_deep_nesting(self):
        """Test recursive generation with deeply nested directories"""
        # Create deeply nested structure
        deep_path = os.path.join(self.content_dir, "a", "b", "c", "d")
        os.makedirs(deep_path)

        # Create markdown file in deep directory
        markdown_content = "# Deep Page\n\nThis is deeply nested."
        markdown_path = os.path.join(deep_path, "deep.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        # Create template
        template_content = (
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate pages recursively
        generate_pages_recursive(self.content_dir, template_path, self.public_dir)

        # Verify deeply nested file was generated
        expected_path = os.path.join(self.public_dir, "a", "b", "c", "d", "deep.html")
        self.assertTrue(os.path.exists(expected_path))

        # Verify content
        with open(expected_path, "r") as f:
            result = f.read()
        self.assertIn("<title>Deep Page</title>", result)
        self.assertIn("<h1>Deep Page</h1>", result)


if __name__ == "__main__":
    unittest.main()
