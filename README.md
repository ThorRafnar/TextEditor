# TextEditor
A simple text editor written in python.

Uses the curses library for TUI

Lines are stored as Ropes (rope.py for implementation of Rope) in a doubly linked list

Current features
- Open a file provided as a command line argument
- Get filename if none is provided
- Navigtion using arrow keys.
- Backspace and enter
- Closing the file and saving with ESC

Roadmap
- Add undo/redo functionality using stacks
- Add syntax highlighting for python (and other languages maybe)

