import unittest

from htmlnode import HTMLNode


class TestHTMLNodeInit(unittest.TestCase):
    def test_stores_all_fields(self):
        child = HTMLNode("span", "child")
        node = HTMLNode("a", "Boot.dev", [child], {"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot.dev")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"href": "https://boot.dev"})

    def test_all_fields_default_to_none(self):
        node = HTMLNode()
        for field in ("tag", "value", "children", "props"):
            with self.subTest(field=field):
                self.assertIsNone(getattr(node, field))

    def test_fields_are_settable_by_keyword(self):
        node = HTMLNode(props={"class": "bold"})
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "bold"})


class TestToHtml(unittest.TestCase):
    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_raises_even_when_fully_populated(self):
        node = HTMLNode("p", "text", [], {"class": "x"})
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestPropsToHtml(unittest.TestCase):
    def test_none_props_returns_empty_string(self):
        self.assertEqual(HTMLNode().props_to_html(), "")

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(HTMLNode(props={}).props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_multiple_props_keep_insertion_order(self):
        node = HTMLNode(
            "a",
            "link",
            None,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" target="_blank"',
        )

    def test_every_prop_is_space_prefixed(self):
        cases = [
            ({"a": "1"}, 1),
            ({"a": "1", "b": "2"}, 2),
            ({"a": "1", "b": "2", "c": "3"}, 3),
        ]
        for props, expected_count in cases:
            with self.subTest(props=props):
                rendered = HTMLNode(props=props).props_to_html()
                self.assertTrue(rendered.startswith(" "))
                self.assertEqual(rendered.count(" "), expected_count)

    def test_empty_value_renders_empty_attribute(self):
        node = HTMLNode(props={"disabled": ""})
        self.assertEqual(node.props_to_html(), ' disabled=""')

    def test_non_string_values_are_stringified(self):
        node = HTMLNode(props={"colspan": 2, "hidden": True})
        self.assertEqual(node.props_to_html(), ' colspan="2" hidden="True"')

    def test_values_are_not_html_escaped(self):
        # Documents current behaviour: props are interpolated verbatim.
        node = HTMLNode(props={"title": 'He said "hi"'})
        self.assertEqual(node.props_to_html(), ' title="He said "hi""')

    def test_does_not_mutate_props(self):
        props = {"href": "https://boot.dev"}
        node = HTMLNode(props=props)
        node.props_to_html()
        self.assertEqual(node.props, {"href": "https://boot.dev"})
        self.assertEqual(props, {"href": "https://boot.dev"})

    def test_is_idempotent_across_calls(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), node.props_to_html())


class TestRepr(unittest.TestCase):
    def test_includes_class_name(self):
        self.assertIn("HTMLNode", repr(HTMLNode()))

    def test_includes_every_field_value(self):
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://boot.dev"})
        rendered = repr(node)
        for expected in ("a", "Boot.dev", "None", "{'href': 'https://boot.dev'}"):
            with self.subTest(expected=expected):
                self.assertIn(expected, rendered)

    def test_empty_node_reports_none_for_each_field(self):
        self.assertEqual(repr(HTMLNode()).count("None"), 4)

    def test_returns_a_string(self):
        self.assertIsInstance(repr(HTMLNode("p", "text")), str)


if __name__ == "__main__":
    unittest.main()
