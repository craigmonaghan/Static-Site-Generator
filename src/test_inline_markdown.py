import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_simple_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(3, len(new_nodes))
        
        self.assertEqual("This is ", new_nodes[0].text)
        self.assertIs(TextType.TEXT, new_nodes[0].text_type)

        self.assertEqual("bold", new_nodes[1].text)
        self.assertIs(TextType.BOLD, new_nodes[1].text_type)

        self.assertEqual(" text", new_nodes[2].text)
        self.assertIs(TextType.TEXT, new_nodes[2].text_type)
        
    
    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(1, len(new_nodes))
        self.assertEqual("Just plain text", new_nodes[0].text)
        self.assertIs(TextType.TEXT, new_nodes[0].text_type)
        
        
    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with an [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)