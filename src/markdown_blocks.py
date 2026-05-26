from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *





def markdown_to_blocks(markdown):
    returned_list = []
    split_list = markdown.split("\n\n")
    for split in split_list:
        if split == "":
            continue
        returned_list.append(split.strip())
    return returned_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        print(f"--- BLOCK ({blocktype}): {repr(block[:80])}")
        if blocktype == BlockType.HEADING:
            text_list = block.split("# ", 1)
            h_length = 1 + len(text_list[0])
            children = text_to_children(text_list[1])  
            child_nodes.append(ParentNode(f"h{h_length}", children))
            print("heading children:", len(children))
        elif blocktype == BlockType.CODE:
            text = block[4:-3]
            html_child = text_node_to_html_node(TextNode(text, TextType.TEXT))
            code_node = ParentNode("code",[html_child])
            child_nodes.append(ParentNode("pre", [code_node]))
        elif blocktype == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = [line.lstrip(">").strip() for line in lines]
            string = " ".join(cleaned)
            children = text_to_children(string)
            child_nodes.append(ParentNode("blockquote", children))
            print("quote children:", len(children), repr(cleaned))
        elif blocktype == BlockType.ULIST:
            lines = block.split("\n")
            child = []
            for line in lines:
                cleaned = line.lstrip("- ").strip()
                children = text_to_children(cleaned)
                child.append(ParentNode("li",children))
            child_nodes.append(ParentNode("ul", child))
            print("ul children:", len(children), repr(cleaned))
        elif blocktype == BlockType.OLIST:
            lines = block.split("\n")
            child = []
            for line in lines:
                cleaned = line[3:]
                children = text_to_children(cleaned)
                child.append(ParentNode("li",children))
            child_nodes.append(ParentNode("ol", child))
            print("ol children:", len(children), repr(cleaned))
        else:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            child_nodes.append(ParentNode("p", children))
            print("p children:", len(children))        
    return ParentNode("div",child_nodes)


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    print(f"  text_to_textnodes({text!r}) → {textnodes}")
    childnodes = []
    for nodes in textnodes:
        childnodes.append(text_node_to_html_node(nodes))
    return childnodes