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
                return Rope(self.data[index])

        elif isinstance(index, slice):
            if self.left and self.right:
                start = index.start
                if index.start is None:
                    if index.step is None or index.step > 0:
                        head = self.left
                    else:
                        head = self.right
                elif (index.start < -self.right.length or
                        0 <= index.start < self.left.length):
                    head = self.left
                    if index.start and index.start < -self.right.length:
                        start += self.right.length
                else:
                    head = self.right
                    if index.start and index.start >= self.left.length:
                        start -= self.left.length

                # TODO: stop = -right.length could be on either subrope.
                # There are two options:
                #   1. tail = left and stop = None (or left.length)
                #   2. tail = right as a '' string, which is removed
                # Currently doing method 2, but I'm on the fence here.
                stop = index.stop
                if index.step is None or index.step > 0:
                    if (index.stop is None or
                            -self.right.length <= index.stop < 0 or
                            index.stop > self.left.length):
                        tail = self.right
                        if index.stop and index.stop > self.left.length:
                            stop -= self.left.length
                    else:
                        if head == self.right:
                            tail = self.right
                            stop = 0
                        else:
                            tail = self.left
                            if index.stop < -self.right.length:
                                stop += self.right.length
                else:
                    if (index.stop is None or
                            index.stop < (-self.right.length - 1) or
                            0 <= index.stop < self.left.length):
                        tail = self.left
                        if index.stop and index.stop < (-self.right.length - 1):
                            stop += self.right.length
                    else:
                        if head == self.left:
                            tail = self.left
                            stop = -1   # Or self.left.length - 1 ?
                        else:
                            tail = self.right
                            if index.stop >= self.left.length:
                                stop -= self.left.length

                # Construct the rope
                if head == tail:
                    return head[start:stop:index.step]
                else:
                    if not index.step:
                        offset = None
                    elif index.step > 0:
                        if start is None:
                            delta = -head.length
                        elif start >= 0:
                            delta = start - head.length
                        else:
                            delta = max(index.start, -self.length) + tail.length

                        offset = delta % index.step
                        if offset == 0:
                            offset = None
                    else:
                        if start is None:
                            offset = index.step + (head.length - 1) % (-index.step)
                        elif start >= 0:
                            offset = index.step + min(start, head.length - 1) % (-index.step)
                        else:
                            offset = index.step + (start + head.length) % (-index.step)

                    if not tail[offset:stop:index.step]:
                        return head[start::index.step]
                    else:
                        return head[start::index.step] + tail[offset:stop:index.step]
            else:
                return Rope(self.data[index])

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

    def reduce(self):
        pass

    def insert(self, index, s):
        pass