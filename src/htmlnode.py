

class HTMLNode:
    def __init__(self, tag: str = None, value:str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        ret = ""

        for key, value in self.props.items():
            ret = ret + f' {key}="{value}"'

        return ret

    def __repr__(self):
        return f'HTMLNode \ntag: {self.tag} \nvalue: {self.value} \nchildren: {self.children} \nprops: {self.props}'
