import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("invalid markdown, unmatched delimiter")
            
            for index, part in enumerate(parts):
                if part == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        if node.text_type is TextType.TEXT:
            ex_images = extract_markdown_images(node.text)
            if not ex_images:
                new_nodes.append(node)
            else:
                current_text_to_split = node.text
                for alt_text, url in ex_images:
                    full_image_markdown = f"![{alt_text}]({url})"
                    parts = current_text_to_split.split(full_image_markdown, maxsplit=1)
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                        current_text_to_split = parts[1]
                if current_text_to_split != "":
                    new_nodes.append(TextNode(current_text_to_split, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        if node.text_type is TextType.TEXT:
            ex_link = extract_markdown_links(node.text)
            if not ex_link:
                new_nodes.append(node)
            else:
                current_text_to_split = node.text
                for link_text, url in ex_link:
                    full_image_markdown = f"[{link_text}]({url})"
                    parts = current_text_to_split.split(full_image_markdown, maxsplit=1)
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                        new_nodes.append(TextNode(link_text, TextType.LINK, url))
                        current_text_to_split = parts[1]
                if current_text_to_split != "":
                    new_nodes.append(TextNode(current_text_to_split, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes





if __name__ == "__main__":
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(extract_markdown_images(text))
    print(extract_markdown_links(text))
    print(text_to_textnodes(text))