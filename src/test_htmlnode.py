import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node_props(self):
        node = HTMLNode(tag="p", props={"style": "color:red"}, value="hello world")
        self.assertEqual(" style=\"color:red\"", node.props_to_html())

    def test_leaf_node_to_html(self):
        leaf = LeafNode(tag="p", value="This is a paragraph of text.")
        leaf2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})

        expected = '<p>This is a paragraph of text.</p>'
        actual = leaf.to_html()
        self.assertEqual(expected, actual)

        expected2 = '<a href="https://www.google.com">Click me!</a>'
        actual2 = leaf2.to_html()
        self.assertEqual(expected2, actual2)

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
