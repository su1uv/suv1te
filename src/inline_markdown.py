import re

from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    splitted: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            splitted.append(node)
            continue
        matches: list[tuple[str, str]] = extract_markdown_images(node.text)
        if len(matches) == 0:
            splitted.append(node)
            continue

        temp_text: str = node.text
        for match in matches:
            temp_list: list[str] = temp_text.split(f"![{match[0]}]({match[1]})", 1)
            if temp_list[0] != "":
                splitted.append(TextNode(temp_list[0], TextType.PLAIN_TEXT))
            splitted.append(TextNode(match[0], TextType.IMAGE, match[1]))
            temp_text = "".join(temp_list[1:])

        if temp_text != "":
            splitted.append(TextNode(temp_text, TextType.PLAIN_TEXT))

    return splitted


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    splitted: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            splitted.append(node)
            continue
        matches: list[tuple[str, str]] = extract_markdown_links(node.text)
        if len(matches) == 0:
            splitted.append(node)
            continue

        temp_text: str = node.text
        for match in matches:
            temp_list: list[str] = temp_text.split(f"[{match[0]}]({match[1]})", 1)
            if temp_list[0] != "":
                splitted.append(TextNode(temp_list[0], TextType.PLAIN_TEXT))
            splitted.append(TextNode(match[0], TextType.LINK, match[1]))
            temp_text = "".join(temp_list[1:])

        if temp_text != "":
            splitted.append(TextNode(temp_text, TextType.PLAIN_TEXT))

    return splitted


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        splitted_text = node.text.split(delimiter)
        for i, v in enumerate(splitted_text):
            if v == "":
                continue
            if i % 2 != 0 and i != 0:
                new_nodes.append(TextNode(v, text_type))
                continue

            new_nodes.append(TextNode(v, TextType.PLAIN_TEXT))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]+)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = re.findall(
        r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]+)\)", text
    )
    return matches
