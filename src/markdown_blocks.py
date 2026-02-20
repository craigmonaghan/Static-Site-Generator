from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    starting_blocks = markdown.split("\n\n")
    blocks = []
    for block in starting_blocks:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks


def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if markdown.startswith("1. "):
        count = 1
        for line in lines:
            if not line.startswith(f"{count}. "):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            p_children = text_to_children(text)
            block_node = ParentNode("p", p_children)
            children.append(block_node)
        
        elif block_type == BlockType.CODE:
            raw = block[4:-3]
            block_node = ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(raw, TextType.TEXT))])])
            children.append(block_node)
    
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level + 1:].strip()
            h_children = text_to_children(text)
            block_node = ParentNode(f"h{level}", h_children)
            children.append(block_node)
        
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = []
            for line in lines:
                cleaned.append(line.lstrip(">").strip())
            text = " ".join(cleaned)
            q_children = text_to_children(text)
            children.append(ParentNode("blockquote", q_children))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line[2:]
                li_children = text_to_children(item_text)
                items.append(ParentNode("li", li_children))
            children.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line.split(". ", 1)[1]
                li_children = text_to_children(item_text)
                items.append(ParentNode("li", li_children))
            children.append(ParentNode("ol", items))

        else:
            raise ValueError(f"unhandled block type:: {block_type}")
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children