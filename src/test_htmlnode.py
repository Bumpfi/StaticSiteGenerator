import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a", "Click me", None, {"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_no_props(self):
        node = HTMLNode("p", "Hello world")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("span", "inline text", None, {"class": "highlight"})
        repr_str = repr(node)
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("span", repr_str)
        self.assertIn("inline text", repr_str)
        self.assertIn("{'class': 'highlight'}", repr_str)


if __name__ == "__main__":
    unittest.main()
