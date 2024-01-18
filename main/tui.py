import curses
import time
from .line_manager import LineManager
from .line_node import LineNode
from .rope import Rope

def main(stdscr):
    SIDE_NUMBER_WIDTH = 4
    SHOULD_ZERO_INDEX = False
    # Initialization
    curses.curs_set(1)  # Make the cursor visible
    stdscr.nodelay(False)  # Make getch() wait for the user to press a key
    stdscr.clear()  # Clear the screen

    # Initialize LineManager
    line_manager = LineManager()
    line_manager.move_cursor(line_manager.head, 0)  # Set cursor at the beginning
    # TODO Implement horizontal and vertical scrolling
    # Main loop
    while True:
        # Inside the main loop
        stdscr.clear()
        for index, line_node in enumerate(line_manager):
            i = index if SHOULD_ZERO_INDEX else index + 1
            line_number = f'{i:<{SIDE_NUMBER_WIDTH - 1}}|'
            line_content = str(line_node.text)  # Assuming `text` is an attribute of LineNode, convert to string if necessary
            stdscr.addstr(index, 0, line_number + line_content)
        y, x = line_manager.get_pos()
        stdscr.move(y, x + SIDE_NUMBER_WIDTH)  # Adjust cursor position to account for the side number width
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