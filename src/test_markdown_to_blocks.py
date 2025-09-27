import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_split(self):
        md = """# This is a heading

This is a paragraph with **bold** text

- item 1
- item 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph with **bold** text",
                "- item 1\n- item 2",
            ],
        )

    def test_ignore_extra_blank_lines(self):
        md = """first

second



third"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["first", "second", "third"])

    def test_strips_whitespace(self):
        md = """   spaced block

next block   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["spaced block", "next block"])


if __name__ == "__main__":
    unittest.main()
