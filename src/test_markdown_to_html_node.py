import unittest

from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_quote_block(self):
        md = "> This is a quote\n> spanning two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_multiple_blocks(self):
        md = "# Heading\n\nThis is a paragraph.\n\n- List item 1\n- List item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul></div>"
        self.assertEqual(html, expected)

    def test_inline_markdown_in_heading(self):
        md = "## Heading with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h2>Heading with <b>bold</b> and <i>italic</i></h2></div>"
        )

    def test_inline_markdown_in_list(self):
        md = "- Item with **bold**\n- Item with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <code>code</code></li></ul></div>",
        )

    def test_inline_markdown_in_quote(self):
        md = "> This is a quote with `code` and **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <code>code</code> and <b>bold</b></blockquote></div>",
        )

    def test_images_and_links_inline(self):
        md = "Here is an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Here is an <img src="https://i.imgur.com/zjjcJKZ.png" alt="image" /> and a <a href="https://boot.dev">link</a></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
