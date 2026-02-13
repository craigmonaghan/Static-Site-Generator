from enum import Enum

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