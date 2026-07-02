import re

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def extract_title(markdown: str) -> str:
    title: list[str] = re.findall(r"(?<!\#)# .*\n", markdown)
    if not title:
        raise Exception("missing h1")
    format_title: str = title[0].rstrip("\n ").lstrip("# ")
    return format_title


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    html_children: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag, children = block_to_html(block_type, block)
        html_children.append(ParentNode(tag, children=children))
    html: ParentNode = ParentNode("div", html_children)
    return html


def block_to_html(block_type: BlockType, block: str) -> tuple[str, list[HTMLNode]]:
    tag: str = ""
    text: str = ""
    children: list[HTMLNode] = []
    grandchildren: list[HTMLNode] = []
    match block_type:
        case BlockType.HEADER:
            tag = header_to_tag(block)
            text = block.lstrip("# ")
            grandchildren = text_to_children(text)
            return (tag, grandchildren)
        case BlockType.QUOTE:
            tag = "blockquote"
            text = block.lstrip("> ").replace("\n", " ")
            grandchildren = text_to_children(text)
            return (tag, grandchildren)
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            text_lines = block.split("\n")
            for line in text_lines:
                line = line.lstrip("- ")
                grandchildren = text_to_children(line)
                children.append(ParentNode("li", children=grandchildren))
            return (tag, children)
        case BlockType.ORDERED_LIST:
            tag = "ol"
            text_lines = block.split("\n")
            for line in text_lines:
                line = line.lstrip("1234567890. ")
                grandchildren = text_to_children(line)
                children.append(ParentNode("li", children=grandchildren))
            return (tag, children)
        case BlockType.CODE:
            tag = "pre"
            text = block.lstrip("```\n").rstrip("```")
            node = TextNode(text, TextType.PLAIN_TEXT)
            leaf_node = text_node_to_html_node(node)
            grandchildren.append(leaf_node)
            children.append(ParentNode("code", children=grandchildren))
            return (tag, children)
        case _:
            tag = "p"
            text = block.replace("\n", " ")
            grandchildren = text_to_children(text)
            return (tag, grandchildren)


def text_to_children(text: str) -> list[HTMLNode]:
    children: list[HTMLNode] = []
    nodes: list[TextNode] = text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(node))

    return children


def header_to_tag(block: str) -> str:
    for i, char in enumerate(block):
        if char != "#":
            return f"h{i}"
    return "h1"
