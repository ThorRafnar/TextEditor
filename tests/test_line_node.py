import unittest
from main.line_node import LineNode
from main.rope import Rope

class TestLineNode(unittest.TestCase):

    def test_initialization(self):
        # Test initialization with a string
        ln = LineNode("hello")
        self.assertEqual(str(ln.text), "hello")

        # Test initialization with a Rope
        rope_text = Rope("hello")
        ln = LineNode(rope_text)
        self.assertEqual(ln.text, rope_text)

    def test_set_text(self):
        # Test setting text with a string
        ln = LineNode()
        ln.set_text("hello")
        self.assertEqual(str(ln.text), "hello")

        # Test setting text with a Rope
        rope_text = Rope("world")
        ln.set_text(rope_text)
        self.assertEqual(ln.text, rope_text)

    def test_insert_text(self):
        # Test inserting text in the middle
        ln = LineNode("hello")
        ln.insert_text(3, "p")
        self.assertEqual(str(ln.text), "helplo")

        # Test inserting text at the beginning
        ln.insert_text(0, "s")
        self.assertEqual(str(ln.text), "shelplo")

        # Test inserting text at the end
        ln.insert_text(len(ln.text), "y")
        self.assertEqual(str(ln.text), "shelploy")

    def test_delete_text(self):
        # Test deleting text in the middle
        ln = LineNode("shelploy")
        ln.delete_text(3, 3)
        self.assertEqual(str(ln.text), "sheoy")

        # Test deleting text from the beginning
        ln.delete_text(0, 1)
        self.assertEqual(str(ln.text), "heoy")

        # Test deleting text from the end
        ln.delete_text(len(ln.text) - 2, 2)
        self.assertEqual(str(ln.text), "he")

if __name__ == '__main__':
    unittest.main()
