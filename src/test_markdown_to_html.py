import unittest

from markdown_to_html import extract_title, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_headers(self):
        md = """
# This is a 1 header

## This is a 2 header

### This is a 3 header

#### This is a 4 header

##### This is a 5 header

###### This is a 6 header

this is a paragraph with **bold** text with
some inline stuff and _italic_ stuff
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a 1 header</h1><h2>This is a 2 header</h2><h3>This is a 3 header</h3><h4>This is a 4 header</h4><h5>This is a 5 header</h5><h6>This is a 6 header</h6><p>this is a paragraph with <b>bold</b> text with some inline stuff and <i>italic</i> stuff</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list item
- This is another list item

1. Here an ordered list item
2. Here another ordered list item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item</li></ul><ol><li>Here an ordered list item</li><li>Here another ordered list item</li></ol></div>",
        )

    def test_paragraphs_with_link(self):
        md = """
This is a [link](https://www.example.com)
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a <a href="https://www.example.com">link</a></p></div>',
        )

    # TODO: Handle images, auto closed tags

    #     def test_paragraphs_with_img(self):
    #         md = """
    # This is a ![image](https://www.example.com/image.png)
    #     """

    #         node = markdown_to_html_node(md)
    #         print(node)
    #         html = node.to_html()
    #         self.assertEqual(
    #             html,
    #             '<div><p>This is a<img src="https://www.example.com/image.png" alt="image"></p></div>',
    #         )

    def test_extract_title(self):
        md = """
# This is a 1 header

## This is a 2 header

### This is a 3 header

#### This is a 4 header

##### This is a 5 header

###### This is a 6 header

this is a paragraph with **bold** text with
some inline stuff and _italic_ stuff
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "This is a 1 header")


if __name__ == "__main__":
    unittest.main()
