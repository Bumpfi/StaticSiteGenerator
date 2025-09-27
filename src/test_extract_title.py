import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        """Test basic H1 header extraction"""
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")

    def test_extract_title_with_whitespace(self):
        """Test H1 header with leading and trailing whitespace"""
        markdown = "#   Hello World   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_with_content_after(self):
        """Test H1 header with content following it"""
        markdown = """# My Title

This is some content after the title.

## Subheading
More content here."""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_extract_title_with_content_before(self):
        """Test H1 header with content before it"""
        markdown = """Some intro text

# The Real Title

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "The Real Title")

    def test_extract_title_ignores_h2(self):
        """Test that H2 headers are ignored"""
        markdown = """## This is H2

# This is H1

## Another H2"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is H1")

    def test_extract_title_ignores_h3_and_beyond(self):
        """Test that H3+ headers are ignored"""
        markdown = """### H3 Header
#### H4 Header
##### H5 Header

# The H1 Title

###### H6 Header"""
        result = extract_title(markdown)
        self.assertEqual(result, "The H1 Title")

    def test_extract_title_first_h1_wins(self):
        """Test that the first H1 header is returned when multiple exist"""
        markdown = """# First Title

Some content here.

# Second Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_extract_title_empty_title(self):
        """Test H1 header with no title text"""
        markdown = "#"
        result = extract_title(markdown)
        self.assertEqual(result, "")

    def test_extract_title_empty_title_with_space(self):
        """Test H1 header with just a space"""
        markdown = "# "
        result = extract_title(markdown)
        self.assertEqual(result, "")

    def test_extract_title_no_h1_raises_exception(self):
        """Test that missing H1 header raises exception"""
        markdown = """## Only H2 headers here
### And H3 headers
Some regular content."""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in markdown")

    def test_extract_title_empty_string_raises_exception(self):
        """Test that empty markdown raises exception"""
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_only_whitespace_raises_exception(self):
        """Test that markdown with only whitespace raises exception"""
        markdown = "   \n\n   \t  "
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_complex_title(self):
        """Test H1 header with complex title including special characters"""
        markdown = "# The Lord of the Rings: A Journey Through Middle-earth!"
        result = extract_title(markdown)
        self.assertEqual(
            result, "The Lord of the Rings: A Journey Through Middle-earth!"
        )

    def test_extract_title_with_inline_formatting(self):
        """Test H1 header with inline markdown formatting"""
        markdown = "# **Bold** and *italic* title"
        result = extract_title(markdown)
        self.assertEqual(result, "**Bold** and *italic* title")

    def test_extract_title_indented_h1(self):
        """Test H1 header with leading whitespace"""
        markdown = "   # Indented Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Indented Title")

    def test_extract_title_no_space_after_hash(self):
        """Test that # without space is not considered H1"""
        markdown = """#NotATitle
## Real H2
#AlsoNotATitle

# Real Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "Real Title")


if __name__ == "__main__":
    unittest.main()
