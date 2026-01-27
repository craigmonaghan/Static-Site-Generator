import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("this is a url", TextType.LINK)
        node2 = TextNode("this is a url", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("https://boot.dev", TextType.LINK)
        node2 = TextNode("https://boott.dev", TextType.LINK)
        self.assertNotEqual(node, node2)
               
    def test_not_eq(self):
        node = TextNode("This is not equal", TextType.TEXT)
        node2 = TextNode("This is not equal", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))
      
if __name__ == "__main__":
    unittest.main()