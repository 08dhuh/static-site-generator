import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a","someurl",None,{"val":"tagsss"})
        node2 = HTMLNode("a","someurl",None,{"val":"tagsss"})
        
        #node = TextNode("This is a text node", TextType.BOLD)
       # node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("a","someurl",None,{"val":"tagsss"})
        node2 = HTMLNode("p","someurl",None,{"val":"tagsss"})
        
        #node = TextNode("not a text node", TextType.IMAGE,"some ulr")
        #node2 = TextNode("italc", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
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
        
    # def test_text(self):
    #     node = TextNode("This is a text node", TextType.PLAIN)
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, None)
    #     self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()