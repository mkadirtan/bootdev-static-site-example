class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key, val in self.props.items():
            props_html += f' {key}="{val}"'
        return props_html

    def __repr__(self):
        children = ""
        if self.children is not None:
            children = "".join(map(lambda x: f"{x}", self.children))
        value = ""
        if self.value is not None:
            value = self.value
        return f"<{self.tag}{self.props_to_html()}>{value}{children}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props, children=children, value=None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is not present")
        if self.children is None or len(self.children) == 0:
            raise ValueError("children is empty")

        inside = ""
        for child in self.children:
            inside += child.to_html()

        return f"<{self.tag}>{inside}</{self.tag}>"
