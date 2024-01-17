import curses

from line_manager import LineManager

def main(stdscr):
    # Initialization
    curses.curs_set(1)  # Make the cursor visible
    stdscr.nodelay(False)  # Make getch() wait for the user to press a key
    stdscr.clear()  # Clear the screen

    # Initialize LineManager
    line_manager = LineManager()
    line_manager.insert_line("")  # Insert a sample line
    line_manager.move_cursor(line_manager.head, 0)  # Set cursor at the beginning

    # Main loop
    while True:
        # Inside the main loop
        stdscr.clear()
        current_line = line_manager.head
        line_num = 0
        while current_line:
            stdscr.addstr(line_num, 0, str(current_line.text))  # Make sure text is converted to string properly
            current_line = current_line.next
            line_num += 1
        stdscr.move(line_manager.get_line_number(line_manager.cursor_line), line_manager.cursor_line_index)
        stdscr.refresh()
        # Handle input
        key = stdscr.getch()
        if key == curses.KEY_UP:
            # Move cursor up
            if line_manager.cursor_line.prev:
                line_manager.cursor_line = line_manager.cursor_line.prev
                line_manager.cursor_line_index = min(line_manager.cursor_line_index, line_manager.cursor_line.text.length)
        elif key == curses.KEY_DOWN:
            # Move cursor down
            if line_manager.cursor_line.next:
                line_manager.cursor_line = line_manager.cursor_line.next
                line_manager.cursor_line_index = min(line_manager.cursor_line_index, line_manager.cursor_line.text.length)
        elif key == curses.KEY_LEFT:
            # Move cursor left
            if line_manager.cursor_line_index > 0:
                line_manager.cursor_line_index -= 1
            elif line_manager.cursor_line.prev:  # Move to the end of the previous line
                line_manager.cursor_line = line_manager.cursor_line.prev
                line_manager.cursor_line_index = line_manager.cursor_line.text.length
        elif key == curses.KEY_RIGHT:
            # Move cursor right
            if line_manager.cursor_line_index < line_manager.cursor_line.text.length:
                line_manager.cursor_line_index += 1
            elif line_manager.cursor_line.next:  # Move to the start of the next line
                line_manager.cursor_line = line_manager.cursor_line.next
                line_manager.cursor_line_index = 0

        elif key == curses.KEY_BACKSPACE or key == 127:
            # Handle backspace (delete character or merge lines)
            if line_manager.cursor_line_index > 0:
                # Delete character at the cursor position
                line_manager.cursor_line.delete_text(line_manager.cursor_line_index - 1, 1)
                line_manager.cursor_line_index -= 1
            elif line_manager.cursor_line.prev:
                # Merge with the previous line
                prev_line = line_manager.cursor_line.prev
                prev_line_length = prev_line.text.length
                prev_line.text += line_manager.cursor_line.text
                line_manager.delete_line(line_manager.cursor_line)
                line_manager.cursor_line = prev_line
                line_manager.cursor_line_index = prev_line_length

        elif key == curses.KEY_ENTER or key == 10:
            # Handle enter (split line or create a new one)
            new_line_text = line_manager.cursor_line.text[line_manager.cursor_line_index:]
            line_manager.cursor_line.text = line_manager.cursor_line.text[:line_manager.cursor_line_index]
            line_manager.insert_line(new_line_text, after_line=line_manager.cursor_line)
            line_manager.move_cursor(line_manager.cursor_line.next, 0)

        elif key >= 32 and key <= 126:  # Printable characters
            # Insert character at the cursor position
            line_manager.cursor_line.insert_text(line_manager.cursor_line_index, chr(key))
            line_manager.cursor_line_index += 1


# Start the curses application
curses.wrapper(main)