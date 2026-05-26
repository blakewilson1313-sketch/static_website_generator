from textnode import *
from htmlnode import *
import re



class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.text = value
        self.children = children
        self.props = props
    

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for prop in self.props:
            string += f' {prop}="{self.props[prop]}"'
        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.text}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.text is None:
            raise ValueError
        if self.tag is None:
            return f"{self.text}"
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.text}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.text}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No Tag")
        if self.children is None or self.children == []:
            raise ValueError("No Children")
        props = self.props_to_html()
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{props}>{child_string}</{self.tag}>"
