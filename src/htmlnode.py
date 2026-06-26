class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None or not self.props:
            return ""

        attributes: str = ""
        for k, v in self.props.items():
            attributes += f' {k}="{v}"'

        return attributes

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("value is missing")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("tag is missing")
        if not self.children:
            raise ValueError("children are missing")

        final_html: str = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            final_html += node.to_html()
        final_html += f"</{self.tag}>"

        return final_html
