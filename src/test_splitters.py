import unittest

from splitters import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Here is a [link1](url1) and another [link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("already image", TextType.IMAGE, "url")
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_no_images_returns_same(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)


if __name__ == "__main__":
    unittest.main()
