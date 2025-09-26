from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode mus have children")

        props_str = "" if self.props is None else f" {self.props_to_html()}"
        result = f"<{self.tag}{props_str}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"

        return result
