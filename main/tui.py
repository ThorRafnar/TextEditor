import curses

from line_manager import LineManager
from line_node import LineNode
from rope import Rope

def main(stdscr):
    # Initialization
    curses.curs_set(1)  # Make the cursor visible
    stdscr.nodelay(False)  # Make getch() wait for the user to press a key
    stdscr.clear()  # Clear the screen

    # Initialize LineManager
    line_manager = LineManager()
    line_manager.insert_line("") # Insert a sample line
    line_manager.move_cursor(line_manager.head, 0)  # Set cursor at the beginning
    # TODO Implement horizontal and vertical scrolling
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
        y, x = line_manager.get_pos()
        stdscr.move(y, x)
        stdscr.refresh()
        # Handle input
        key = stdscr.getch()
        if key == curses.KEY_UP:
            line_manager.try_move_up()
        elif key == curses.KEY_DOWN:
            line_manager.try_move_down()
        elif key == curses.KEY_LEFT:
            line_manager.try_move_left()
        elif key == curses.KEY_RIGHT:
            line_manager.try_move_right()

        elif key == curses.KEY_BACKSPACE or key == 127:
            line_manager.handle_backspace()

        elif key == curses.KEY_ENTER or key == 10:
            line_manager.handle_enter()

        elif key >= 32 and key <= 126:  # Printable characters
            line_manager.handle_character(chr(key))
            


# Start the curses application
curses.wrapper(main)