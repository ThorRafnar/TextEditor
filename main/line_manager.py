from typing import Union
from line_node import LineNode
from rope import Rope


class LineManager:
    def __init__(self):
        self.head = None  # Start of the lines
        self.tail = None  # End of the lines
        self.cursor_line = None  # Line where the cursor is currently located
        self.cursor_line_index = 0  # The line number of the cursor_line
    
    def get_line_number(self, line_node):
        line_num = 0
        current_node = self.head
        while current_node and current_node != line_node:
            line_num += 1
            current_node = current_node.next
        return line_num

    def insert_line(self, text: Union[Rope, str] = '', after_line: LineNode=None):
        new_line = LineNode(text)
        if after_line is None:  # Insert at the beginning
            new_line.next = self.head
            self.head = new_line
            if new_line.next:
                new_line.next.prev = new_line
            if self.tail is None:
                self.tail = new_line
        else:  # Insert after the specified line
            new_line.next = after_line.next
            new_line.prev = after_line
            after_line.next = new_line
            if new_line.next:
                new_line.next.prev = new_line
            if self.tail == after_line:
                self.tail = new_line

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
