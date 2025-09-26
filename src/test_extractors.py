import unittest

from extractors import extract_markdown_images, extract_markdown_links


class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![first](url1) and ![second](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "url1"), ("second", "url2")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a [link](https://example.com)")
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_no_false_image_as_link(self):
        text = "![notalink](url)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
