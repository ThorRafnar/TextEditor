import unittest
import sys

sys.path.append('../')
from main.rope import Rope

class TestRopeMethods(unittest.TestCase):

    def test_init_throws_type_error(self):
        self.assertRaises(TypeError, Rope, {})
        self.assertRaises(TypeError, Rope, ("this is", "not a string", "but a tuple"))
        self.assertRaises(TypeError, Rope, "Two strings", "Are not good")
    
    def test_init_base(self):
        Rope()

    def test_init_accepts_string(self):
        Rope("String")

    def test_init_accepts_list_of_strings(self):
        Rope(["List ", "of ", "strings"])

    def test_init_accepts_empty_list(self):
        Rope([])

    def test_str_when_constructed_from_string(self):
        my_string = "Hello, world"
        self.assertEqual(str(Rope(my_string)), my_string)

    def test_str_for_long_string(self):
        my_string = "Hello, world! What a good day to be alive when we can supporty such long strings!!!"
        self.assertEqual(str(Rope(my_string)), my_string)

    def test_equal_ropes_with_different_constructors(self):
        one = Rope("Hello, world")
        two = Rope(["Hel", "lo,", " wo", "rld"])
        self.assertEqual(one, two)

    def test_unequal_ropes(self):
        one = Rope("Hello, world")
        two = Rope(["Good morning Viet Nam"])
        self.assertNotEqual(one, two)

    def test_add_ropes(self):
        one = Rope("Hello,")
        two = Rope([" world"])
        self.assertEqual(str(one + two), "Hello, world")

    def test_len(self):
        my_string = "Hello, world"
        self.assertEqual(len(Rope(my_string)), len(my_string))
    
    def test_repr(self):
        rope = Rope("Hello, world")
        rope.__repr__()

    def test_get_item(self):
        rope = Rope("Hello, world")
        self.assertEqual(rope[0], 'H')
        self.assertEqual(rope[-1], 'd')
        self.assertEqual(rope[2], 'l')
        self.assertEqual(rope[-2], 'l')

    def test_get_item_index_error(self):
        rope = Rope("Hello, world")
        with self.assertRaises(IndexError):
            print(rope[25])

    def test_height(self):
        rope = Rope("Hello, world")
        print(rope._height())
        other = Rope("Good morning Viet Nam! What the fuck is up")
        combined = rope + other
        print(combined._height())
        print(combined.left._height())
        print(combined.right._height())
        print(rope._is_balanced())
        print(other._is_balanced())
        print(combined._is_balanced())

    def test_split(self):
        rope = Rope("Hello, world")
        one, two = rope.split(5)
        print(one)

if __name__ == '__main__':
    unittest.main()