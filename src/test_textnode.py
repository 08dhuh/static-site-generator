import unittest

from textnode import TextNode, TextType
from helper import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("not a text node", TextType.IMAGE,"some ulr")
        node2 = TextNode("italc", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
    TextNode("This is text with a ", TextType.PLAIN),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.PLAIN),
])

if __name__ == "__main__":
    unittest.main()