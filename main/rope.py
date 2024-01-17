from __future__ import annotations
from typing import Union, List, Optional

class Rope:
    def __init__(self, data: Union[str, List[str]] = '') -> None:
        # STRING BASED CONSTRUCTOR
        if isinstance(data, str):
            self.left = None
            self.right = None
            self.data = data
            self.length = len(data)
        # LIST BASED CONSTRUCTOR
        elif isinstance(data, list):
            # Assert every item is a string
            for item in data:
                if not isinstance(item, str):
                    raise TypeError(f'Unsupported data type: {type(item)} found in list. Supported data types: list[str], str')
            # Construct Rope based on length
            if len(data) == 0:
                self.__init__()
            elif len(data) == 1:
                # String based constructor handles splitting up if too long
                self.__init__(data[0])
            else:
                # Round-up division
                mid = len(data) // 2 + (len(data) % 2 > 0)
                self.left = Rope(data[:mid])
                self.right = Rope(data[mid:])
                self.data = ''
                self.length = self.left.length + self.right.length
        else:
            raise TypeError(f'Unsupported data type: {type(data)}. Supported data types: list[str], str')
        self.current = self

    def __eq__(self, other: Rope) -> bool:
        return str(self) == str(other)

    def __add__(self, other: Union[Rope, str, List[str]]) -> Rope:
        # If `other` is not a Rope, convert it to a Rope
        if not isinstance(other, Rope):
            other = Rope(other)
        
        new_rope = Rope()
        new_rope.left = self
        new_rope.right = other
        new_rope.data = ''  # Internal nodes shouldn't hold data directly
        new_rope.length = len(self) + len(other)  # Calculate the combined length
        new_rope = new_rope.balance()  # Balance the new Rope
        
        return new_rope

    def __len__(self) -> int:
        if self.left is not None and self.right is not None:
            return len(self.left) + len(self.right)
        else:
            return(len(self.data))

    def __getitem__(self, index) -> Rope:
        if isinstance(index, int):
            if self.left and self.right:
                if index < -self.right.length:
                    subindex = index + self.right.length
                elif index >= self.left.length:
                    subindex = index - self.left.length
                else:
                    subindex = index

                if index < -self.right.length or 0 <= index < self.left.length:
                    return self.left[subindex]
                else:
                    return self.right[subindex]
            else:
                try:
                    return Rope(self.data[index])
                except IndexError:
                    raise IndexError
        else:
            raise TypeError("Unsupported indexing")

    def __repr__(self, level: int=0, prefix: str="Root: ") -> str:
        # Representation for the current node
        result = "  " * level + prefix + repr(self.data) + "\n"
        
        # If the current node has children, recursively represent them
        if self.left is not None:
            result += self.left.__repr__(level + 1, "Left: ")
        if self.right is not None:
            result += self.right.__repr__(level + 1, "Right: ")
        
        return result

    def __str__(self) -> str:
        if self.left is not None and self.right is not None:
            return self.left.__str__() + self.right.__str__()
        else:
            return self.data

    def __iter__(self) -> Rope:
        return self

    def __next__(self) -> str:
        if self.current:
            if self.left is not None and self.right is not None:
                try:
                    return next(self.left)
                except StopIteration:
                    self.current = self.right
                return next(self.right)
            else:
                self.current = None
                return self.data
        else:
            raise StopIteration

    def next(self) -> str:
        return self.__next__()
    
    def split(self, index: int) -> (Rope, Rope):
        if index < 0:
            index += len(self)
        if index < 0 or index > self.length:
            raise IndexError("Index out of bounds")
        if index == 0:
            return Rope(''), self
        if index == self.length:
            return self, Rope('')
        
        # Base case: If the current node is a leaf node
        if self.left is None and self.right is None:
            left_part = Rope(self.data[:index])
            right_part = Rope(self.data[index:])
            return left_part, right_part

        # Recursive case: Split occurs in the left or right child
        if self.left and index <= len(self.left):
            left_part, extra = self.left.split(index)
            right_part = extra + self.right if self.right else extra
        else:
            extra, right_part = self.right.split(index - len(self.left))
            left_part = self.left + extra

        return left_part, right_part

    def balance_factor(self) -> int:
        left_height = self.left._height() if self.left else 0
        right_height = self.right._height() if self.right else 0
        return left_height - right_height

    def balance(self) -> Rope:
        bf = self.balance_factor()
        if bf > 1:  # Left heavy
            if self.left and self.left.balance_factor() < 0:
                # Left-Right Case
                self.left = self.left.rotate_left()
            # Left-Left Case
            return self.rotate_right()
        elif bf < -1:  # Right heavy
            if self.right and self.right.balance_factor() > 0:
                # Right-Left Case
                self.right = self.right.rotate_right()
            # Right-Right Case
            return self.rotate_left()
        # Update the length and return the node itself if it's already balanced
        self.update_length()
        return self

    def rotate_left(self):
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        self.update_length()
        new_root.update_length()
        return new_root

    def rotate_right(self):
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        self.update_length()
        new_root.update_length()
        return new_root

    def update_length(self) -> None:
        self.length = len(self.data) + (self.left.length if self.left else 0) + (self.right.length if self.right else 0)

    def _height(self):
        if self.left is None and self.right is None:
            return 0
        left_height = self.left._height() + 1 if self.left else 0
        right_height = self.right._height() + 1 if self.right else 0
        return max(left_height, right_height)

    def insert(self, index, s) -> Rope:
        new_rope = Rope(s)

        if index == 0:
            # Insert at the start of the Rope
            combined = new_rope + self
        elif index == self.length:
            # Append at the end of the Rope
            combined = self + new_rope
        else:
            # Split the Rope and insert the new text
            left, right = self.split(index)
            combined = left + new_rope + right
        
        return combined.balance()

    def delete(self, index: int, length: int) -> Rope:
        if index < 0 or index + length > self.length:
            raise IndexError("Index out of bounds")
        
        # Split the rope at the start of the range to delete
        left, temp = self.split(index)
        
        # Split the temp rope at the end of the range to delete
        _, right = temp.split(length)
        
        # Combine the left and right parts, effectively deleting the middle part
        result = left + right
        
        return result