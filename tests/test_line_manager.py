import unittest
from main.line_manager import LineManager
from main.line_node import LineNode
from main.rope import Rope

class TestLineManager(unittest.TestCase):
    def setUp(self):
        # Set up a LineManager instance and other resources before each test
        self.line_manager = LineManager()

    def tearDown(self):
        # Reset the LineManager instance if needed
        self.line_manager = None


    def test_empty_initialization(self):
        # Test initializing LineManager with no file path
        self.assertEqual(type(self.line_manager.head), LineNode)
        self.assertIsNotNone(self.line_manager.tail)
        self.assertEqual(self.line_manager.cursor_line_index, 0)

    def test_len(self):
        self.line_manager = LineManager()
        self.line_manager.insert_line("First line")
        self.line_manager.insert_line("Second line")
        self.assertEqual(len(self.line_manager), 3)

    def test_iteration(self):
        # Test inserting text and 2 lines, and iterating over them
        self.line_manager = LineManager()
        self.line_manager.insert_text("Initial line")
        self.line_manager.insert_line("First line")
        self.line_manager.insert_line("Second line")
        for line in self.line_manager:
            print(line)
            self.assertGreater(len(line), 1)
    
    def test_enter_empty_lines(self):
        self.line_manager = LineManager()
        self.line_manager.handle_enter()
        self.line_manager.handle_enter()
        self.assertEqual(len(self.line_manager), 3)
        for line in self.line_manager:
            self.assertEqual(str(line), "")

    def test_insert_text_at_beginning(self):
        # Test inserting a line at the beginning of the document
        self.line_manager.insert_text("First line")
        self.assertIsNotNone(self.line_manager.head)
        self.assertEqual(str(self.line_manager.head.text), "First line")
        self.assertEqual(self.line_manager.head, self.line_manager.cursor_line)

    def test_handle_enter_at_beginning_of_line(self):
        # Test pressing Enter at the beginning of a line
        self.line_manager.insert_text("Line before enter")
        self.line_manager.cursor_line_index = 0
        self.line_manager.handle_enter()
        self.line_manager.handle_enter()
        
        self.assertEqual(len(self.line_manager), 3)
        self.assertEqual(self.line_manager.head.text, "")  # Assuming a space is added for an empty new line
        self.assertEqual(self.line_manager.head.next.text, "")
        self.assertEqual(self.line_manager.head.next.next.text, "Line before enter")
        for index, line in enumerate(self.line_manager):
            if index < 2:
                self.assertEqual(str(line), "")
            else:
                self.assertEqual(str(line), "Line before enter")
    
    def test_enter_text_and_press_enter_at_beginning(self):
        # This is functionality from hell :)
        self.line_manager.insert_text("Line before enter")
        self.assertEqual(str(self.line_manager.cursor_line), "Line before enter")
        self.line_manager.cursor_line_index = 0
        self.line_manager.handle_enter()
        self.line_manager.handle_enter()
        self.line_manager.handle_enter()
        self.line_manager.try_move_up()
        self.line_manager.insert_text("Test")
        print(self.line_manager)

    def test_try_move_up(self):
        # Create a situation where the cursor is on the second line
        self.line_manager.insert_line("Line 1")
        self.line_manager.insert_line("Line 2")
        self.line_manager.move_cursor(self.line_manager.head.next, 0)  # Move cursor to the beginning of "Line 2"
        self.assertEqual(self.line_manager.get_pos(), (1, 0))
        # Now try to move up
        self.line_manager.try_move_up()
        self.assertEqual(self.line_manager.cursor_line, self.line_manager.head)  # Cursor should now be on "Line 1"
        self.assertEqual(self.line_manager.cursor_line_index, 0)  # Index should be 0



if __name__ == '__main__':
    unittest.main()
