from __future__ import annotations
from typing import Union, List, Optional

from rope import Rope

class LineNode:
    def __init__(self, text: Union[Rope, str, List[str]]=''):
        if not isinstance(text, Rope):
            self.text = Rope(text)  # Use your Rope class to store line text
        else:
            self.text = text
        self.next = None  # Pointer to the next line
        self.prev = None  # Pointer to the previous line

    def insert_text(self, index: int, text: Union[Rope, str, List[str]]):
        self.text = self.text.insert(index, text)

    def delete_text(self, index: int, length: int):
        self.text = self.text.delete(index, length)