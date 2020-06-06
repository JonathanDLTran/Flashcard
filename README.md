# Flashcard
Adaptable flash card system with search indexing

## Editor
Inside the flash card system is a text editor to add notes and change cards. The system was built from scratch using
curses as a base foundation. No curses textpads were used as that's like cheating; also, the textpad doesn't support
any of the operations I implemented anyways, and so I had to build my own data structures and operations instead.
### Features
Standard Typing Features
- Insert any character in Regular ASCII keyboard (type)
- Delete (delete)
- Newline (return)
- Tab (tab) : The user can tab, which will add spaces up to the next multiple of tab spacing

Movement
- Left, Right, Up, Down Scroll (arrow keys)
- Top of document, bottom of doc, farthest left, farthest right scroll (fn arrow keys)

Exit
- Exit (Ctrl - G) 

Copying/Cutting/Pasting
- Cut and Paste (Ctrl - X Ctrl - P)
- Copy and Paste (Ctrl - D Ctrl - P)
- Copy All (Ctrl-A)
- Escape Copies and Cuts (Esc)

Style
- Highlight (Ctrl H)
- Bold (Ctrl B)
- Underline (Ctrl U)

Editor Information
- Page count, line count, row count

Coloring:
- Black, Red, Cyan, Green and Yellow Text colors
- Commands are ctrl N, ctrl P, ctrl L, ctrl W, ctrl E

### Future
- Non Ascii Character insertion (wider character type), Meta Key support
- Ctrl F search
- Ctrl S save into json
- Ctrl Z undo
- Ctrl Y redo 
Word Copy
Line Copy
Scroll Up by Page
Scroll Down by Page

### No Planned Support
- Ctrl C (This is always going to stop execution)
- other Ctrl + keys where no ascii code is given
- Overwrite mode 


