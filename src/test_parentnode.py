import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_example_from_assignment(self):
        """Test the exact example given in the assignment"""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_no_tag_raises_error(self):
        """Test that missing tag raises ValueError"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("tag", str(context.exception))

    def test_no_children_raises_error(self):
        """Test that missing children raises ValueError with different message"""
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("children", str(context.exception))
        # Make sure it's a different message from the tag error
        self.assertNotIn("tag", str(context.exception))

    def test_empty_children_list(self):
        """Test with empty children list (should work, just empty content)"""
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_single_child(self):
        """Test with single child"""
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>text</span></div>")

    def test_multiple_children(self):
        """Test with multiple children"""
        children = [
            LeafNode("b", "Bold"),
            LeafNode("i", "Italic"),
            LeafNode(None, "Plain text"),
        ]
        parent = ParentNode("p", children)
        expected = "<p><b>Bold</b><i>Italic</i>Plain text</p>"
        self.assertEqual(parent.to_html(), expected)

    def test_nested_parent_nodes(self):
        """Test deeply nested ParentNodes"""
        deepest = LeafNode("strong", "Deep text")
        level2 = ParentNode("em", [deepest])
        level1 = ParentNode("span", [level2])
        root = ParentNode("div", [level1])
        expected = "<div><span><em><strong>Deep text</strong></em></span></div>"
        self.assertEqual(root.to_html(), expected)

    def test_mixed_parent_and_leaf_children(self):
        """Test parent with both ParentNode and LeafNode children"""
        leaf1 = LeafNode("b", "Bold")
        nested_leaf = LeafNode("i", "Italic")
        parent_child = ParentNode("span", [nested_leaf])
        leaf2 = LeafNode(None, "Plain")

        root = ParentNode("div", [leaf1, parent_child, leaf2])
        expected = "<div><b>Bold</b><span><i>Italic</i></span>Plain</div>"
        self.assertEqual(root.to_html(), expected)

    def test_with_props(self):
        """Test ParentNode with properties"""
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        result = parent.to_html()
        # Should contain the props and the child content
        self.assertIn("<span>content</span>", result)
        self.assertIn("class", result)
        self.assertIn("container", result)
        self.assertIn("id", result)
        self.assertIn("main", result)

    def test_complex_nesting_scenario(self):
        """Test a complex real-world-like HTML structure"""
        # Create: <article><h1>Title</h1><p><b>Bold</b> and <i>italic</i> text.</p></article>
        title = LeafNode("h1", "Title")
        bold = LeafNode("b", "Bold")
        plain1 = LeafNode(None, " and ")
        italic = LeafNode("i", "italic")
        plain2 = LeafNode(None, " text.")
        paragraph = ParentNode("p", [bold, plain1, italic, plain2])
        article = ParentNode("article", [title, paragraph])

        expected = "<article><h1>Title</h1><p><b>Bold</b> and <i>italic</i> text.</p></article>"
        self.assertEqual(article.to_html(), expected)

    def test_constructor_sets_value_to_none(self):
        """Test that ParentNode constructor sets value to None"""
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child])
        self.assertIsNone(parent.value)

    def test_constructor_inheritance(self):
        """Test that ParentNode properly inherits from HTMLNode"""
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child])
        self.assertIsInstance(parent, HTMLNode)
        self.assertEqual(parent.tag, "div")
        self.assertIsNotNone(parent.children)
        if parent.children is not None:
            self.assertEqual(len(parent.children), 1)

    def test_multiple_levels_of_nesting(self):
        """Test multiple levels of nesting with various combinations"""
        # Level 4: deepest leaf
        deep_leaf = LeafNode("code", "code_text")

        # Level 3: parent containing the deep leaf
        level3 = ParentNode("pre", [deep_leaf])

        # Level 2: parent with multiple children including level 3
        level2_leaf = LeafNode("span", "span_text")
        level2 = ParentNode("div", [level2_leaf, level3])

        # Level 1: root with level 2 and additional leaf
        root_leaf = LeafNode("h2", "heading")
        root = ParentNode("section", [root_leaf, level2])

        expected = "<section><h2>heading</h2><div><span>span_text</span><pre><code>code_text</code></pre></div></section>"
        self.assertEqual(root.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
