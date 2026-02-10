import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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
    def test_split_no_images(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        expected_output = [node]
        result = split_nodes_image([node])
        self.assertListEqual(result, expected_output)
    

    def test_split_non_text_node_image(self):
        node = TextNode("link", TextType.LINK, "https://example.com/image.png")
        expected_output = [node]
        result = split_nodes_image([node])
        self.assertListEqual(result, expected_output)


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_no_links(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        expected_output = [node]
        result = split_nodes_link([node])
        self.assertListEqual(result, expected_output)
    

    def test_split_non_text_node_link(self):
        node = TextNode("Image alt", TextType.IMAGE, "https://example.com/image.png")
        expected_output = [node]
        result = split_nodes_link([node])
        self.assertListEqual(result, expected_output)
