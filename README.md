# Flashcard
Adaptable flash card system with search indexing

# Editor
Inside the flash card system is a text editor to add notes and change cards. The system was built from scratch using
curses as a base foundation. No curses textpads were used as that's like cheating; also, the textpad doesn't support
any of the operations I implemented anyways, and so I had to build my own data structures and operations instead.

### Requirements:
- Python 3.7 
- Python distribution of curses, json, 
- Latest MAC OS, no guarantee for Windows or Linux

### Features
#### Standard Typing Features
- Insert any character in Regular ASCII keyboard (type)
- Delete (delete)
- Newline (return)
- Tab (tab) : The user can tab, which will add spaces up to the next multiple of tab spacing (can set tab spacing)

#### Movement
- Left, Right, Up, Down Scroll (arrow keys)
- Top of document, bottom of doc, farthest left, farthest right scroll (fn arrow keys)
- Scroll Up by 1 Page (ctrl F)
- Scroll Down by 1 Page (shift tab)

#### Exit
- Exit (Ctrl - G) 

#### Copying/Cutting/Pasting
- Cut and Paste (Ctrl - X Ctrl - P)
- Copy and Paste (Ctrl - D Ctrl - P)
- Copy All (Ctrl-A)
- Escape Copies and Cuts (Esc)

#### Style
- Highlight (Ctrl H)
- Bold (Ctrl B)
- Underline (Ctrl U)

#### Editor Information
- Page count, line count, row count

#### Coloring:
- Black, Red, Cyan, Green and Yellow Text colors
- Commands are ctrl N, ctrl P, ctrl L, ctrl W, ctrl E

#### Bookmarking:
- 5 lines can be bookmarked and reset (fn 1 - 5)
- Jump back to those bookmarks (fn 6 - 10)

#### History:
Save: Ctrl-S to save into a local json file
Redo: Ctrl-R to redo an immediate undo
Undo: Ctrl-T to undo up to undo limit number of undos (can set undo limit)

#### Macro:
- Keystroke macro and run macro (no recursive macros e.g embedded keystroke macros in a keystroke macros)
- takes insert, delete, tab, newline for keystroke macros
- Fn 12 to record and end record
- Ctrl _ to run macro

### Find and Search:
- Fn Return is used to find
- Enter to finish the find statement
- In edit-find mode, will search and highlight all occurrences of find statement
- FN Returnto leave edit-find mode and remove all highlights, clears find buffer

### Wide Characters
- Non Ascii Character insertion (wider character type), Meta/Alt/Option Key support 

### Future Plans
- Ctrl R Replace text with new text
- Word Copy
- Line Copy


### No Planned Support
- Ctrl C (This is always going to stop execution)
- Ctrl I italics (Not supported by curses in python)
- other Ctrl + keys where no ascii code is given
- Overwrite mode 
- Syntax Highlighting (another project perhaps?, build a language?) [[Next Planned Project is to construct a language, build an front end to lex and parse, and add intepreter, plus add syntax color]]

# Language

## Lexer
## Parser
## Interpreter

## Support
- Assignment
- Ignore
- if - elif - else statements
- For Loops
- While Loops
- Functions with Closures defined at time of definition
- Function application
- Return statements
- External functions: len(), get(), set(), mem(), print()

## TYPES
- Ints
- Floats
- String
- List
- Tuple
- Dictionaries
- Structs (runtime declared, no compile time type declaractions)

## Type Checker
I have branched the language into a new c-like language, rather than the previous formerly Python like language. As such, now there is type checking. Currently, int, bool, string, float, tuple, list, dictionary, typedef unions (with new support for union types for union creation), typedef structs (and struct creation), return, ignore, if, for, while, function, external functions, and function application type checking is implemented for the language.  Further extension might add some type inference with the unification algorithm for generic types, specified like 
````
`a
````
or 
````
`t
````
However, there is no plan to extend generic types or polymorphic types beyond an intepreter phase, and certainly not to the IR or final compiler.


## IR (RISC-like intermediate representation) (In planning stage / In progress / TODO)
The next step is to develop a translation of the language from the C-like version to an IR which is a higher level Risc language. This IR will be based on three argument assembly instructions and will feature ops like add, ld, st, etc. Instead of using registers, variables will be kept with the function names. Temporary variables are introduced as necessary. If needed, control flow graphs and redundancy DAGs may be added, as provisions for optimization. 

## Code emission (Preliminary Non-IR Emission Finished / IR Based Emission - Not yet planned)
Current code emission translates semantically analyzed code straight into RISC-V assembly code, without the intermediate representation. This was due to a misunderstanding of the purpose and structure of the IR. Following this basic translation, an IR will be developed to facilitate higher level concepts and optimization. 

The final planned step is to develop code emission from the IR to RISC-V assembly code. This will probably be more straightforward than what happens for the IR translation phase. Register spilling into the stack will be liberally used. Space layout may not be optimal. Code is NOT OPTIMIZED in any fashion.  

Code emission currently generates RISC V code for a core subset of the language defined earlier. This was finished by Septermber 1st, 2020.

