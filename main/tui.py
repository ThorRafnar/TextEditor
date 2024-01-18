import curses
import sys
from .line_manager import LineManager
from .line_node import LineNode
from .rope import Rope

def main(stdscr):
    SIDE_NUMBER_WIDTH = 4
    SHOULD_ZERO_INDEX = False
    CTRL_Q = ord('q') - 96  # Ctrl+Q
    CTRL_S = ord('s') - 96  # Ctrl+S
    ESC = 27
    

    # Initialization
    curses.curs_set(1)  # Make the cursor visible
    stdscr.nodelay(False)  # Make getch() wait for the user to press a key
    stdscr.clear()  # Clear the screen

    filename = sys.argv[1] if len(sys.argv) > 1 else ""
    # If no filename was provided as a command-line argument, prompt the user for a filename
    if not filename:
        # Clear the screen and prompt for filename
        stdscr.clear()
        stdscr.addstr(0, 0, "Please enter the filename: ")
        stdscr.refresh()
        
        # Enable echoing of characters
        curses.echo()
        while True:
            char = stdscr.getch(1, len(filename))  # Get character at position (1, len of current input)
            if char == 10:  # Enter key (newline) pressed, end input
                break
            elif char == 27:  # ESC key pressed, cancel input
                filename = ""
                break
            elif char == curses.KEY_BACKSPACE or char == 127:  # Handle backspace
                filename = filename[:-1]
                stdscr.addstr(1, 0, " " * (len(filename) + 1))  # Clear line
                stdscr.addstr(1, 0, filename)  # Redraw current filename
            else:
                # Append character to filename and display
                filename += chr(char)
            stdscr.refresh()

        # Disable echoing of characters
        curses.noecho()

    # Initialize LineManager
    line_manager = LineManager(file_path=filename)
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

        elif key == CTRL_S:
            # Handle save content to file
            line_manager.save_content()
            stdscr.addstr(len(line_manager) + 2, 0, "Content saved!")
        
        elif key == CTRL_Q:
            # Handle quit
            line_manager.save_content()  # Optionally save before quitting
            break  # Break out of the loop to end the program

        elif key == ESC:
            # Handle quit
            line_manager.save_content()  # Optionally save before quitting
            break  # Break out of the loop to end the program
                    


# Start the curses application
curses.wrapper(main)