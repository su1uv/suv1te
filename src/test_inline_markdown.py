import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    # Test extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_link(self):
        matches = extract_markdown_images(
            "This is a link [image](https://www.google.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_mult_images(self):
        matches = extract_markdown_images(
            "This is an ![image](images_one.com) an here is another ![second image](here another)"
        )
        self.assertListEqual(
            [("image", "images_one.com"), ("second image", "here another")], matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is an [link](www.markdown.example)")
        self.assertListEqual([("link", "www.markdown.example")], matches)

    def test_extract_markdown_links_with_image(self):
        matches = extract_markdown_links("This is not a ![link](this.com)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_mult_links(self):
        matches = extract_markdown_links(
            "This [text](hast.two) links [inside](example.com)"
        )
        self.assertListEqual([("text", "hast.two"), ("inside", "example.com")], matches)

    # Test split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test split_nodes_image
    def test_split_images_no_text_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test split_nodes_image
    def test_split_images_text_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with text in the end",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with text in the end", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    # Test split_nodes_link
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test split_nodes_link
    def test_split_links_no_text_start(self):
        node = TextNode(
            "[image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test split_nodes_link
    def test_split_links_text_end(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) with text in the end",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with text in the end", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    # Test split_nodes_delimiter
    def test_one_code(self):
        nodes_to_split: list[TextNode] = [
            TextNode("This is a `code` text", TextType.PLAIN_TEXT),
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes_to_split, "`", TextType.CODE_TEXT),
            splitted_nodes,
        )

    # Test split_nodes_delimiter
    def test_one_italic(self):
        nodes_to_split: list[TextNode] = [
            TextNode("This is a _code_ text", TextType.PLAIN_TEXT),
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes_to_split, "_", TextType.ITALIC_TEXT),
            splitted_nodes,
        )

    # Test split_nodes_delimiter
    def test_no_plain(self):
        nodes_to_split: list[TextNode] = [
            TextNode("This is not plain", TextType.BOLD_TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes_to_split, "**", TextType.BOLD_TEXT),
            nodes_to_split,
        )

    # Test split_nodes_delimiter
    def test_mult_bold(self):
        nodes_to_split: list[TextNode] = [
            TextNode("This is **multi** bold letters **node**.", TextType.PLAIN_TEXT),
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("multi", TextType.BOLD_TEXT),
            TextNode(" bold letters ", TextType.PLAIN_TEXT),
            TextNode("node", TextType.BOLD_TEXT),
            TextNode(".", TextType.PLAIN_TEXT),
        ]
        result_nodes = split_nodes_delimiter(nodes_to_split, "**", TextType.BOLD_TEXT)
        self.assertEqual(result_nodes, splitted_nodes)

    # Test split_nodes_delimiter
    def test_with_start_delimiter(self):
        nodes_to_split: list[TextNode] = [
            TextNode("**this** is a delimiter in the start", TextType.PLAIN_TEXT),
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("this", TextType.BOLD_TEXT),
            TextNode(" is a delimiter in the start", TextType.PLAIN_TEXT),
        ]
        result_nodes = split_nodes_delimiter(nodes_to_split, "**", TextType.BOLD_TEXT)
        self.assertEqual(result_nodes, splitted_nodes)

    # Test split_nodes_delimiter
    def test_with_end_delimiter(self):
        nodes_to_split: list[TextNode] = [
            TextNode("this has a delimiter in the _end_", TextType.PLAIN_TEXT)
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("this has a delimiter in the ", TextType.PLAIN_TEXT),
            TextNode("end", TextType.ITALIC_TEXT),
        ]
        result_nodes = split_nodes_delimiter(nodes_to_split, "_", TextType.ITALIC_TEXT)
        self.assertEqual(result_nodes, splitted_nodes)

    # Test split_nodes_delimiter
    def test_with_start_end_delimiter(self):
        nodes_to_split: list[TextNode] = [
            TextNode("`this has` a start and `end delimiter`", TextType.PLAIN_TEXT)
        ]
        splitted_nodes: list[TextNode] = [
            TextNode("this has", TextType.CODE_TEXT),
            TextNode(" a start and ", TextType.PLAIN_TEXT),
            TextNode("end delimiter", TextType.CODE_TEXT),
        ]
        result_nodes = split_nodes_delimiter(nodes_to_split, "`", TextType.CODE_TEXT)
        self.assertEqual(result_nodes, splitted_nodes)


if __name__ == "__main__":
    unittest.main()
