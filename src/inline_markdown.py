from textnode import *
from htmlnode import *
import re




def text_node_to_html_node(textnode):
    if textnode.text_type == TextType.TEXT:
        return LeafNode(None, textnode.text)
    elif textnode.text_type == TextType.BOLD:
        return LeafNode("b", textnode.text)
    elif textnode.text_type == TextType.ITALIC:
        return LeafNode("i", textnode.text)
    elif textnode.text_type == TextType.CODE:
        return LeafNode("code", textnode.text)
    elif textnode.text_type == TextType.LINK:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    elif textnode.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
    else: 
        raise Exception("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:    
        if node.text_type != TextType.TEXT:
             new_nodes.append(node)
             continue
        node_list = node.text.split(delimiter)
        if len(node_list) % 2 == 0:
            raise Exception("Delimiter not in Node")    
        for i in range(0, len(node_list)):
            if node_list[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(node_list[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_list[i],text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:    
        if node.text_type != TextType.TEXT:
             new_nodes.append(node)
             continue
        image_list = extract_markdown_images(node.text)
        if len(image_list) == 0:
            new_nodes.append(node)
            continue
        image_len = len(image_list)
        node_text = node.text
        node_list = []
        for i in range(0, image_len):
            node_list.append(node_text.split(f"![{image_list[i][0]}]({image_list[i][1]})")[0])
            if i + 1 == image_len:
                node_list.append(node_text.split(f"![{image_list[i][0]}]({image_list[i][1]})")[1])
            else:
                node_text = node_text.split(f"![{image_list[i][0]}]({image_list[i][1]})")[1]

        for i in range(0, len(node_list)):
            if node_list[i] != "":
                new_nodes.append(TextNode(node_list[i], TextType.TEXT))
            if i < image_len:
                new_nodes.append(TextNode(image_list[i][0], TextType.IMAGE, image_list[i][1]))

    return new_nodes


def split_nodes_link(old_nodes):  
    new_nodes = []
    for node in old_nodes:    
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        link_list = extract_markdown_links(node.text)
        link_len = len(link_list)
        if link_len == 0:
            new_nodes.append(node)
            continue

        node_text = node.text
        node_list = []
        for i in range(0, link_len):
            node_list.append(node_text.split(f"[{link_list[i][0]}]({link_list[i][1]})")[0])
            if i + 1 == link_len:
                node_list.append(node_text.split(f"[{link_list[i][0]}]({link_list[i][1]})")[1])
            else:
                node_text = node_text.split(f"[{link_list[i][0]}]({link_list[i][1]})")[1]

        for i in range(0, len(node_list)):
            if node_list[i] != "":
                new_nodes.append(TextNode(node_list[i], TextType.TEXT))
            if i < link_len:
                new_nodes.append(TextNode(link_list[i][0], TextType.LINK, link_list[i][1]))

    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes