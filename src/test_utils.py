import unittest
from utils import split_nodes_delimiter
from textnode import TextNode, text_type_text, text_type_code


class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ]

        self.assertEqual(expected_nodes, new_nodes)
