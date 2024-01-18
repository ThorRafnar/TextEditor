from __future__ import annotations
from typing import Union, List, Optional

from .rope import Rope

class LineNode:
    def __init__(self, text: Union[Rope, str, List[str]]=''):
        if not isinstance(text, Rope):
            self.text = Rope(text)  # Use your Rope class to store line text
        else:
            self.text = text
        self.next = None  # Pointer to the next line
        self.prev = None  # Pointer to the previous line

    def __len__(self):
        return len(self.text)
    
    def __str__(self):
        return str(self.text)
    
    def set_text(self, text: Union[Rope, str, List[str]]) -> None:
        if isinstance(text, Rope):
            self.text = text
        else:
            self.text = Rope(text)

    def __bool__(self) -> bool: # Needed to overload bool to return True if the object exists to handle prev and next when navigating
         # Consider a LineNode to be truthy if the node itself exists, regardless of its content
        return True if self is not None else False

    def insert_text(self, index: int, text: Union[Rope, str, List[str]]):
        self.text = self.text.insert(index, text)

    def delete_text(self, index: int, length: int):
        self.text = self.text.delete(index, length)