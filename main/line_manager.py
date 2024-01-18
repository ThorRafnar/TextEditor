from typing import Union, Optional
from .file_handler import FileHandler
from .line_node import LineNode
from .rope import Rope


class LineManager:
    def __init__(self, file_path=""):
        self.file_handler = FileHandler(file_path)
        self.head = None  # Start of the lines
        self.tail = None  # End of the lines
        self.cursor_line = None  # Line where the cursor is currently located
        self.cursor_line_index = 0  # The line number of the cursor_line
        self.load_content()
    
    def __len__(self):
        """Returns the number of lines managed by LineManager."""
        count = 0
        current_node = self.head
        while current_node is not None:
            count += 1
            current_node = current_node.next
        return count

    def load_content(self):
        """Loads the content from the file into the linked list."""
        self.head = self.file_handler.read_file()
        # Set cursor_line and tail
        self.cursor_line = self.head
        temp_node = self.head
        while temp_node is not None:
            self.tail = temp_node
            temp_node = temp_node.next

    def save_content(self):
        """Saves the content from the linked list back to the file."""
        self.file_handler.write_file(self.head)

    def __iter__(self):
        """Allows iteration over the lines managed by LineManager."""
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next

    def __str__(self) -> str:
        ret = []
        for line in self:
            ret.append(str(line))
        return str(ret)


    def get_line_number(self, line_node):
        line_num = 0
        current_node = self.head
        while current_node and current_node != line_node:
            line_num += 1
            current_node = current_node.next
        return line_num

    def insert_line(self, text: Union[LineNode, Rope, str] = '', after_line: LineNode=None):
        new_line = text if isinstance(text, LineNode) else LineNode(text)
        if after_line is None:  # Insert at the beginning
            new_line.next = self.head
            if self.head:  # Ensure the old head's prev pointer is updated
                self.head.prev = new_line
            self.head = new_line
            if not self.tail:  # If the list was empty, new_line is now also the tail
                self.tail = new_line
        else:  # Insert after the specified line
            new_line.next = after_line.next
            new_line.prev = after_line
            if new_line.next:  # Update the prev pointer of the next node
                new_line.next.prev = new_line
            after_line.next = new_line
            if not self.tail or self.tail == after_line:  # Update tail if needed
                self.tail = new_line

    def handle_enter(self):
        # Handle enter (split line or create a new one)
        cursor_line = self.cursor_line
        cursor_line_index = self.cursor_line_index

        if cursor_line_index == 0:
            # Create a new line with the current line's content
            new_line = LineNode(cursor_line.text)
            # Insert the new line after the current line
            self.insert_line(new_line, after_line=cursor_line)
            # Clear the current line's text
            cursor_line.text = Rope(" ")
            cursor_line.delete_text(0, 1)
            # Move the cursor to the start of the new line
            self.move_cursor(new_line, 0)
            

        elif cursor_line_index < len(cursor_line.text):
            # Split the current line at the cursor position
            left_part, right_part = cursor_line.text.split(cursor_line_index)
            cursor_line.text = left_part
            new_line = LineNode(right_part)
            self.insert_line(new_line, after_line=cursor_line)
            # Move the cursor to the start of the new line
            self.move_cursor(new_line, 0)
        else:
            # Cursor is at the end of the line, create a new empty line below
            new_line = LineNode('')
            self.insert_line(new_line, after_line=cursor_line)
            # Move the cursor to the new line
            self.move_cursor(new_line, 0)


    def insert_text(self, text: Union[str, Rope, list[str]], index: Optional[int]=None):
        if index:
            self.cursor_line_index = index
        for char in text:
            self.handle_character(char)
        
    def handle_character(self, character):
        # Insert character at the cursor position
        self.cursor_line.insert_text(self.cursor_line_index, character)
        self.cursor_line_index += 1

    def try_move_right(self):
        # Move cursor right
        if self.cursor_line_index < self.cursor_line.text.length:
            self.cursor_line_index += 1
        elif self.cursor_line.next:  # Move to the start of the next line
            self.cursor_line = self.cursor_line.next
            self.cursor_line_index = 0

    def try_move_left(self):
        # Move cursor left
        if self.cursor_line_index > 0:
            self.cursor_line_index -= 1
        elif self.cursor_line.prev:  # Move to the end of the previous line
            self.cursor_line = self.cursor_line.prev
            self.cursor_line_index = self.cursor_line.text.length

    def try_move_down(self):
        # Move cursor down
        if self.cursor_line.next:
            self.cursor_line = self.cursor_line.next

    def try_move_up(self):
        # Move cursor up
        if self.cursor_line.prev:
            self.cursor_line = self.cursor_line.prev

    def get_pos(self) -> (int, int):
        y = self.get_line_number(self.cursor_line)
        x = 0
        if self.cursor_line is not None:
            x = min(self.cursor_line_index, len(self.cursor_line))
        return y, x 

    def handle_backspace(self):
        # Handle backspace (delete character or merge lines)
        if self.cursor_line_index > 0:
            # Delete character at the cursor position
            self.cursor_line.delete_text(self.cursor_line_index - 1, 1)
            self.cursor_line_index -= 1
        # Merge with the previous line
        elif self.cursor_line.prev:
            prev_line = self.cursor_line.prev
            prev_line_length = prev_line.text.length
            prev_line.text += self.cursor_line.text

            # Update pointers to link the lines correctly
            prev_line.next = self.cursor_line.next
            if self.cursor_line.next:
                self.cursor_line.next.prev = prev_line

            self.delete_line(self.cursor_line)
            self.cursor_line = prev_line
            self.cursor_line_index = prev_line_length

    def delete_line(self, line: LineNode):
        if line is None:
            return

        prev_line = line.prev
        next_line = line.next

        if prev_line is not None:
            prev_line.next = next_line
        if next_line is not None:
            next_line.prev = prev_line

        # If the line being deleted is the cursor line, move the cursor to the next line
        if line == self.cursor_line:
            self.move_cursor(next_line, 0)

    def move_cursor(self, new_line: LineNode, new_index: int):
        self.cursor_line = new_line
        self.cursor_line_index = new_index
