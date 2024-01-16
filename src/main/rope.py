class Rope(object):
    def __init__(self, data=''):
        try:
            # STRING BASED CONSTRUCTOR
            if isinstance(data, str):
                if len(data) > 4:
                    # For longer strings, split it down the middle and call list based constructor
                    mid = len(data) // 2 + (len(data) % 2 > 0)
                    split_list = [data[:mid], data[mid:]]
                    self.__init__(split_list)
                else:
                    self.left = None
                    self.right = None
                    self.data = data
                    self.length = len(data)
            # LIST BASED CONSTRUCTOR
            elif isinstance(data, list):
                # Assert every item is a string
                for item in data:
                    if not isinstance(item, str):
                        raise TypeError('Unsupported data type. Supported data types: list[str], str, not whatever')
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
                raise TypeError('Unsupported data type. Supported data types: list[str], str')
        except:
            raise TypeError('Unsupported data type. Supported data types: list[str], str')
        
        self.current = self

    def __eq__(self, other):
        return str(self) == str(other)

    def __add__(self, other):
        if isinstance(other, Rope):
            r = Rope()
            r.left = self
            r.right = other
            r.length = self.length + other.length
            r.current = self
            r.balance()
            return r
        else:
            try:
                return self.__add__(Rope(other))
            except Exception as e:
                e.add_note(f'Unable to construct rope using {type(other)}, supported types: str, list[str]')
                raise

    def __len__(self):
        if self.left is not None and self.right is not None:
            return len(self.left) + len(self.right)
        else:
            return(len(self.data))
        
    def _height(self):
        if self.left is not None and self.right is not None:
            return 1 + max(self.left._height(), self.right._height())
        else:
            return 0
        
    def _is_balanced(self):
        if self.left is not None and self.right is not None:
            if abs(self.left._height() - self.right._height()) > 1:
                return False
            return self.left._is_balanced() and self.right._is_balanced()
        else:
            return True

    def __getitem__(self, index):
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

    def __repr__(self):
        if self.left and self.right:
            return f'{"(" if self.left else ""}{self.left.__repr__()} + {self.right.__repr__(),}{")" if self.right else ""}'
        else:
            return "Rope('{}')".format(self.data)

    def __str__(self):
        if self.left is not None and self.right is not None:
            return self.left.__str__() + self.right.__str__()
        else:
            return self.data

    def __iter__(self):
        return self

    def __next__(self):
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

    def next(self):
        return self.__next__()
    
    def split(self, index):
        if self is None:
            return None, None

        if index == 0:
            return None, self

        if index >= len(self):
            return self, None

        if index < len(self.left):
            left, right = self.left.split(index)
            new_node = self.right
            new_node.left = left
            new_node.right = self.right
            new_node.weight = self.weight - len(left)
            self.right = None
            self.weight = len(self.left)
            return new_node, self
        elif index == len(self.left):
            return self, self.right
        else:
            left = self.left
            right, remainder = self.right.split(index - len(self.left) - 1)
            self.left = None
            self.right = remainder
            self.weight = len(self.right)
            return left, self

    def balance(self):
        # TODO Implement
        pass

    def insert(self, index, s):
        # TODO Implement
        pass