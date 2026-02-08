import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
  
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_html_text(self):
        node = TextNode("plain", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertIsNone(html.tag)
        self.assertEqual(html.value, "plain")
        self.assertIsNone(html.props)

    def test_text_to_html_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold")

    def test_text_to_html_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic")

    def test_text_to_html_code(self):
        node = TextNode("code", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "code")

    def test_text_to_html_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Click me")
        self.assertEqual(html.props, {"href": "https://example.com"})

    def test_text_to_html_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "https://example.com/img.png", "alt": "alt text"})

    def test_text_to_html_invalid_type_raises(self):
        node = TextNode("weird", "not-a-real-type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
     
if __name__ == "__main__":
    unittest.main()