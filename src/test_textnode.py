import unittest

from textnode import TextNode, TextType


class TestTextType(unittest.TestCase):
    def test_member_values(self):
        cases = [
            (TextType.TEXT, "text"),
            (TextType.BOLD, "bold"),
            (TextType.ITALIC, "italic"),
            (TextType.CODE, "code"),
            (TextType.LINK, "link"),
            (TextType.IMAGE, "image"),
        ]
        for member, expected_value in cases:
            with self.subTest(member=member):
                self.assertEqual(member.value, expected_value)

    def test_lookup_by_value_returns_same_member(self):
        self.assertIs(TextType("bold"), TextType.BOLD)

    def test_unknown_value_raises(self):
        with self.assertRaises(ValueError):
            TextType("underline")


class TestTextNodeInit(unittest.TestCase):
    def test_stores_all_fields(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(node.text, "Boot.dev")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://boot.dev")

    def test_url_defaults_to_none(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)


class TestTextNodeEq(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_matching_urls(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_eq_holds_for_every_text_type(self):
        for text_type in TextType:
            with self.subTest(text_type=text_type):
                node = TextNode("same text", text_type)
                node2 = TextNode("same text", text_type)
                self.assertEqual(node, node2)

    def test_equal_nodes_are_distinct_objects(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertIsNot(node, node2)

    def test_not_eq_when_text_differs(self):
        node = TextNode("first", TextType.TEXT)
        node2 = TextNode("second", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_when_text_type_differs(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_when_url_differs(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_when_only_one_url_is_none(self):
        node = TextNode("Boot.dev", TextType.LINK)
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_to_non_textnode_values(self):
        node = TextNode("This is a text node", TextType.TEXT)
        others = [
            "This is a text node",
            None,
            42,
            ("This is a text node", TextType.TEXT, None),
            {"text": "This is a text node"},
        ]
        for other in others:
            with self.subTest(other=other):
                self.assertNotEqual(node, other)

    def test_eq_is_reflexive(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node)

    def test_eq_is_symmetric(self):
        node = TextNode("alt text", TextType.IMAGE, "https://boot.dev/logo.png")
        node2 = TextNode("alt text", TextType.IMAGE, "https://boot.dev/logo.png")
        self.assertTrue(node == node2)
        self.assertTrue(node2 == node)

    def test_ne_operator_follows_eq(self):
        node = TextNode("first", TextType.TEXT)
        node2 = TextNode("first", TextType.TEXT)
        node3 = TextNode("second", TextType.TEXT)
        self.assertFalse(node != node2)
        self.assertTrue(node != node3)


class TestTextNodeRepr(unittest.TestCase):
    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            repr(node), "TextNode(This is a text node, TextType.BOLD, None)"
        )

    def test_repr_with_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(
            repr(node), "TextNode(Boot.dev, TextType.LINK, https://boot.dev)"
        )

    def test_repr_of_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(, TextType.TEXT, None)")


if __name__ == "__main__":
    unittest.main()
