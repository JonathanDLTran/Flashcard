FRONT = 0
BACK = 1
FORWARD = 2
REAR = 3
FOLLOWING = 4
LAST = 5
SKIP = 'skip'

QUESTION = 'QUESTION:'
ANSWER = 'ANSWER:'
END = 'END'

RATE_SCALE_LIST = [0, 1, 2, 3, 4, 5]
QUIT = 'quit'
HELP = 'help'
CORRECT = 'correct'
INCORRECT = 'incorrect'
SKIP = 'skip'
SPACE = " "

INVALID_COMMAND = "You did not enter a valid command. Trying again. "

SEPARATOR = "###########################"


RIGHT = "right"
LEFT = "left"

################# VIEW RELATED CONSTANTS #############

RIGHT_POINT = "\u261E"
LEFT_POINT = "\u261C"
UP_POINT = "\u261D"
DOWN_POINT = "\u261F"
STAR = "\u2606"

CLEAR_SCREEN = "\033c"

NROWS = 24
NCOLS = 80

SPLIT_SEQUENCE = "$$$!!!$$$"
SPLIT_MARKER = "$$$###$$$"

HISTORY = "\u269C"
SCIENCE = "\u269B"
MUSIC = "\u266C"
RELIGION = "\u26E9"
CHEMISTRY = "\u2697"
MATH = "\u2230"
PHYSICS = "\u2622"
SPORTS = "\u26BE"
NAVAL = "\u2693"
MILITARY = "\u2694"
MEDECINE = "\u2695"
GEOGRAPHY = "\u26F0"
LITERATURE = "\u204B"

DELETE = "\u2620"

######### KEY PRESSES ##########
UP = 259
DOWN = 258
RIGHT = 261
LEFT = 260
DELETE = 127
RETURN = 10
ENTER = RETURN
LINEFEED = RETURN

LINE_LENGTH = 70
NUM_LINES = 10

EDITOR_START_CHAR = " "

GO_LEFT = 262  # fn <-
GO_RIGHT = 360  # fn ->
GO_TOP = 339  # fn up arrow
GO_BOTTOM = 338  # fn down arrow

COPY = 4  # ctrl + D
CUT = 24  # ctrl + X
PASTE = 22  # ctrl + V
FIND = 6  # ctrl + F
COPY_ALL = 1  # ctrl + A
HIGHLIGHT = 263  # ctrl + H
BOLD = 2  # ctrl + B
UNDERLINE = 21  # ctrl + U
# ctrl + Q is 17 NOT WORK
# ctrl + Z NOT WORK
# ctrl + Y NOT WORK

TAB = 9
TAB_SIZE = 4  # must be less than line length


ESCAPE = 27  # ESC - to escape a copy or cut, or delete a paste save

EXIT_EDITOR = 7  # ctrl + G

# Bookmarks
NUM_BOOKMARKS = 5
SETB1 = 265  # fn 1
SETB2 = 266
SETB3 = 267
SETB4 = 268
SETB5 = 269
JUMPB1 = 270  # fn 6
JUMPB2 = 271
JUMPB3 = 272
JUMPB4 = 273
JUMPB5 = 274

STRIKE_THROUGH = '\u0336'

COLOR_RED = 14  # ctrl N
COLOR_CYAN = 16  # ctrl P
COLOR_GREEN = 12  # ctrl L
COLOR_YELLOW = 23  # ctrl W
COLOR_BLACK = 5  # ctrl E

SAVE = 11  # ctrl K

SAVE_TRACK_LENGTH = 50

UNDO = 20  # ctrl T
REDO = 18  # ctrl R

MACRO_RECORD = 276  # fn 12
MACRO_RUN = 31  # ctrl _

UP_ONE_PAGE = 6  # ctrl F
DOWN_ONE_PAGE = 353  # shift-tab = 353
