from __future__ import annotations
from html.parser import HTMLParser
import re
from typing import Iterator


class HtmlNode:
    """Stores one node of the dependency-free public transport HTML tree."""

    def __init__(
        self,
        tag: str,
        attrs: dict[str, str],
        parent: HtmlNode | None = None
    ) -> None:
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children: list[HtmlNode | str] = []

    def iter_nodes(self) -> Iterator[HtmlNode]:
        """Yields this node and all descendant nodes in document order."""
        yield self
        for child in self.children:
            if isinstance(child, HtmlNode):
                yield from child.iter_nodes()

    def find_all(
        self,
        tag: str | None = None,
        class_name: str | None = None
    ) -> list[HtmlNode]:
        """Returns descendants matching a tag and CSS class."""
        return [
            node for node in self.iter_nodes()
            if node is not self
            and (tag is None or node.tag == tag)
            and (class_name is None or node.has_class(class_name))
        ]

    def find(
        self,
        tag: str | None = None,
        class_name: str | None = None
    ) -> HtmlNode | None:
        """Returns the first descendant matching a tag and CSS class."""
        return next(iter(self.find_all(tag, class_name)), None)

    def has_class(self, class_name: str) -> bool:
        """Checks whether the node contains a CSS class."""
        return class_name in self.attrs.get('class', '').split()

    def own_text(self) -> str:
        """Returns normalized text stored directly in this node."""
        return normalize_text(' '.join(
            child for child in self.children if isinstance(child, str)
        ))

    def text(self) -> str:
        """Returns normalized text stored in this node and its descendants."""
        parts: list[str] = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                parts.append(child.text())
        return normalize_text(' '.join(parts))


class HtmlDocumentParser(HTMLParser):
    """Builds a small DOM tree with Python's standard HTML parser."""

    _VOID_TAGS = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = HtmlNode('document', {})
        self._stack = [self.root]

    def handle_starttag(self, tag: str, attrs) -> None:
        node = HtmlNode(
            tag.lower(),
            {str(key): str(value or '') for key, value in attrs},
            self._stack[-1]
        )
        self._stack[-1].children.append(node)
        if tag.lower() not in self._VOID_TAGS:
            self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in self._VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self._stack[-1].children.append(data)


def parse_html(html: str) -> HtmlNode:
    """Parses an HTML string into a traversable document tree."""
    parser = HtmlDocumentParser()
    parser.feed(html)
    parser.close()
    return parser.root


def normalize_text(value: str) -> str:
    """Collapses whitespace in source text."""
    return re.sub(r'\s+', ' ', value or '').strip()
