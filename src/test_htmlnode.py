import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node: HTMLNode = HTMLNode("p", "This is a test paragraph")
        node2: HTMLNode = HTMLNode("p", "This is a test paragraph")
        self.assertEqual(str(node), str(node2))

    def test_value_not_eq(self):
        node = HTMLNode("p", "This is not a test paragraph")
        node2 = HTMLNode("p", "This is a test paragraph")
        self.assertNotEqual(node.value, node2.value)

    def test_props_to_html(self):
        props: dict[str, str] = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "google here", props=props)
        formatted_props = node.props_to_html()
        self.assertEqual(
            formatted_props, ' href="https://www.google.com" target="_blank"'
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mult_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2 p")
        child_node3 = LeafNode("p", "child3 p")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><p>child2 p</p><p>child3 p</p></div>",
        )

    def test_to_html_with_mult_children_and_grandchildren(self):
        grandchildren_node = LeafNode("span", "grandchild")
        grandchildren_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("div", [grandchildren_node, grandchildren_node2])
        child_node2 = ParentNode("section", [grandchildren_node2, grandchildren_node])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span>grandchild</span><p>grandchild2</p></div><section><p>grandchild2</p><span>grandchild</span></section></div>",
        )

    def test_to_html_with_mult_children_props(self):
        child_node = LeafNode("span", "child", props={"classname": "hello"})
        child_node2 = LeafNode("p", "child2 p", props={"classname": "hello2"})
        child_node3 = LeafNode("p", "child3 p")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span classname="hello">child</span><p classname="hello2">child2 p</p><p>child3 p</p></div>',
        )

    def test_to_html_with_mult_children_and_grandchildren_props(self):
        grandchildren_node = LeafNode(
            "span", "grandchild", props={"classname": "hello"}
        )
        grandchildren_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode(
            "div",
            [grandchildren_node, grandchildren_node2],
            props={"classname": "helloparent"},
        )
        child_node2 = ParentNode("section", [grandchildren_node2, grandchildren_node])
        parent_node = ParentNode(
            "div", [child_node, child_node2], props={"classname": "helloparentparent"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div classname="helloparentparent"><div classname="helloparent"><span classname="hello">grandchild</span><p>grandchild2</p></div><section><p>grandchild2</p><span classname="hello">grandchild</span></section></div>',
        )


if __name__ == "__main__":
    unittest.main()
