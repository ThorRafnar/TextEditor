from .line_node import LineNode

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """Reads a file and converts it into a linked list of ropes."""
        head = None
        current_node = None
        
        try:
            with open(self.file_path, 'r') as file:
                # Check the file manually or use a simple Python script
                for line in file:
                    new_node = LineNode(line.rstrip('\n'))  # Remove newline characters
                    if not head:
                        head = new_node
                        current_node = head
                    else:
                        current_node.next = new_node
                        new_node.prev = current_node
                        current_node = new_node
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist. A new file will be created.")
            head = LineNode("")  # Create an empty node if file doesn't exist

        return head  # Return the head of the linked list

    def write_file(self, head):
        """Writes the contents of a linked list of ropes back to a file."""
        with open(self.file_path, 'w') as file:
            current_node = head
            while current_node:
                file.write(str(current_node.text) + '\n')  # Convert Rope to string and write to file
                current_node = current_node.next

if __name__ == '__main__':
    # Check the file manually or use a simple Python script
    with open('main/testFile.txt', 'r') as file:
        content = file.read()
        print(content)  # Verify that this prints the file content

