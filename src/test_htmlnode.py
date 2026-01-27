import unittest

from htmlnode import HTMLNode, LeafNode
class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "hello", None, {"class": "greeting"})
        self.assertEqual("HTMLNode(tag=h1, value=hello, children=None, props={'class': 'greeting'})", repr(node)) 
        
    
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "hello")
        self.assertEqual("", node.props_to_html())
        
    
    def test_props_to_html_with_props(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)     
        
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )


    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
   

if __name__ == "__main__":
    unittest.main()