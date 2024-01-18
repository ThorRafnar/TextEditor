import unittest
import timeit
import sys

sys.path.append('../')
from main.rope import Rope

class TestRopeMethods(unittest.TestCase):

    def test_init_throws_type_error(self):
        self.assertRaises(TypeError, Rope, {})
        self.assertRaises(TypeError, Rope, ("this is", "not a string", "but a tuple"))
        self.assertRaises(TypeError, Rope, "Two strings", "Are not good")
        self.assertRaises(TypeError, Rope, ["A list with strings", 1, 2, "and ints","are not good"])
    
    def test_init_base(self):
        Rope()

    def test_init_accepts_string(self):
        Rope("String")

    def test_init_accepts_list_of_strings(self):
        Rope(["List ", "of ", "strings"])

    def test_init_accepts_empty_list(self):
        Rope([])

    def test_empty_string(self):
        rope = Rope('')
        self.assertEqual(str(rope), "")

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
        rope = one + two
        self.assertEqual(str(rope), str(one) + str(two))

    def test_add_rope_and_string(self):
        one = Rope("Hello,")
        two = " world"
        rope = one + two
        self.assertEqual(str(rope), str(one) + str(two))
    
    def test_add_rope_and_list_string(self):
        one = Rope("Hello,")
        two = [" wo", "rld"]
        rope = one + two
        self.assertEqual(str(rope), "Hello, world")

    def test_add_rope_and_int_throws_type_error(self):
        one = Rope("Hello,")
        two = 1
        with self.assertRaises(TypeError):
            rope = one + two

    def test_len(self):
        my_string = "Hello, world"
        self.assertEqual(len(Rope(my_string)), len(my_string))
    
    def test_repr(self):
        rope = Rope("Hello, world")
        print(rope.__repr__())
        self.assertEqual(rope.__repr__(), "Root: 'Hello, world'\n")

    def test_get_item(self):
        rope = Rope("Hello, world")
        self.assertEqual(rope[0], 'H')
        self.assertEqual(rope[-1], 'd')
        self.assertEqual(rope[2], 'l')
        self.assertEqual(rope[-2], 'l')

    def test_get_item_with_larger_rope(self):
        rope = Rope(["These ", "are ", "many ", "strings. ", "This", " rope", " should", " be", " taller!"])
        self.assertEqual(rope[0], 'T')
        self.assertEqual(rope[-1], '!')
        self.assertEqual(rope[2], 'e')
        self.assertEqual(rope[-2], 'r')
        self.assertEqual(rope[6], 'a')
        self.assertEqual(rope[10], 'm')
    
    def test_get_item_raises_type_error(self):
        rope = Rope(["These ", "are ", "many ", "strings. ", "This", " rope", " should", " be", " taller!"])
        with self.assertRaises(TypeError):
            print(rope['1'])

    def test_get_item_index_error(self):
        rope = Rope("Hello, world")
        with self.assertRaises(IndexError):
            print(rope[25])

    def test_split(self):
        rope = Rope("Hello, world")
        left, right = rope.split(5)
        self.assertEqual(str(left), "Hello")
        self.assertEqual(str(right), ", world")
        self.assertEqual(len(left) + len(right), len(rope))

    def test_split_out_of_bounds(self):
        rope = Rope("Hello, world")
        with self.assertRaises(IndexError):
            left, right = rope.split(50)

    def test_insert(self):
        rope = Rope("Good Viet nam")
        rope = rope.insert(4, " morning")
        self.assertEqual(str(rope), "Good morning Viet nam")

    def test_back_insert(self):
        rope = Rope("Hello, ")
        rope = rope.insert(len(rope), "world")
        self.assertEqual(str(rope), "Hello, world")
    
    def test_front_insert(self):
        rope = Rope("world")
        rope = rope.insert(0, "Hello, ")
        self.assertEqual(str(rope), "Hello, world")

    def test_repeated_adds(self):
        rope = Rope()
        for word in ["Hel", "lo,", " wo", "rld", "Hel", "lo,", " wo", "rld", "Hel", "lo,", " wo", "rld", "Hel", "lo,", " wo", "rld"]:
            rope += word
        self.assertEqual(str(rope), "Hello, worldHello, worldHello, worldHello, world")

    def test_performance(self, insert_index=5, insert_str='abc', iterations=100, length=100):
        repeats = 5
        # Setup code template
        setup_code_template = """
from main.rope import Rope
import random
import string

length = {length}  # Define the length of the large string
base_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
rope = Rope(base_str)
insert_str = "{insert_str}"
        """

        # Code snippets for insertion
        base_str_test_code = """
new_str = base_str
for i in range({iterations}):  # Number of inserts
    new_str = new_str[:{insert_index}] + insert_str + new_str[{insert_index}:]
        """

        rope_test_code = """
for i in range({iterations}):  # Number of inserts
    rope = rope.insert({insert_index}, insert_str)
        """

        # Format the setup code and test code with specific parameters
        setup_code = setup_code_template.format(length=length, insert_str=insert_str)
        
        rope_test_code = rope_test_code.format(insert_index=insert_index, iterations=iterations)
        base_str_test_code = base_str_test_code.format(insert_index=insert_index, iterations=iterations)
        # Time the base str insertions
        base_str_time = timeit.timeit(stmt=base_str_test_code, setup=setup_code, number=repeats)

        # Time the Rope insertions
        rope_time = timeit.timeit(stmt=rope_test_code, setup=setup_code, number=repeats)

        # Print the results
        print(f"Insert Index: {insert_index}, Insert String: '{insert_str}', Iterations: {iterations}, String_length: {length}")
        print(f"Average time for base str insertions: {base_str_time / repeats} seconds")
        print(f"Average time for Rope insertions: {rope_time / repeats} seconds")
        print("-------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()