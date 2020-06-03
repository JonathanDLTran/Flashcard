import Constants
import curses
import traceback
from curses import textpad

"""
edit.py provides the data structures and associated
functions to edit

Essentially functions as a mini text editor
Meant to be used as a plug in addition to the flash card system as an
an editor to fix up cards and cards, as well as to add user notes

Opertions:
Planned:
Insert character(s)
Delete character(s)
Scroll Up
Scroll Down
Scroll Left
Scroll Right
Enter (\n)
FUTURE/OPTIONAL
[opt] HOTKEYING/CTRL+Keys
[opt] Copy and Paste
[opt] Cut and Paste
[opt] Help
[opt] Far Right
[opt] Far Left
[opt] Top
[opt] Bottom
NO SUPPORT PLANNED;
Overwrite characters


REPRESENTATION INVARIANT/CLASS INVARIANT

String Buffer List:
1. Each String is at most 80 characters long
2. If a string has a \n or a \r in it, even if it is less than 80 characters
in length, the data is sent is sent to the next line instead
3. Each string must be stored in the same order it was stored in
"""


def split_text(text):
    """
    split_text(text) splits text into a list of strings satisfying the Representation
    Invariant

    PROPERTY: INverse of Join text
    REQUIRES: Split text to initialize string buffer list data structure
    """
    def split_text_helper(text, str_list):
        l = len(text)
        if l <= Constants.LINE_LENGTH:
            return split_at_newline(text, str_list)
        i = 0
        while (i < l):
            if (i == (Constants.LINE_LENGTH - 1)):
                first_half = text[0: (i + 1)]
                second_half = text[(i + 1): l]
                return split_text_helper(second_half, str_list + [first_half])
            elif (text[i] == "\n" or text[i] == "\r"):
                first_half = text[0: (i + 1)]
                second_half = text[(i + 1): l]
                return split_text_helper(second_half, str_list + [first_half])
            i += 1

    return split_text_helper(text, [])


def split_at_newline(text, str_list):
    """
    split_at_newline(text, str_list) splits text into constituent strings in
    a list separated by \n or \r

    If text is empty, returns empty list

    REQUIRES: text has less than or equal to 80 characters including all \n and \r
    """
    if text == "":
        return str_list

    l = len(text)
    i = 0
    while (i < l):
        if (text[i] == "\n") or (text[i] == "\r"):
            remainder = text[(i + 1): l]
            cut_portion = text[0:(i + 1)]
            return split_at_newline(remainder, str_list + [cut_portion])
        i += 1
    return str_list + [text]


def join_text(str_list):
    """
    join_text(text) joins list of strings into a string of text

    PROPERTY: INverse of split_text
    """
    return "".join(str_list)


def insert(c, x, y, str_list):
    """
    insert(c, x, y, str_list) inserts a character c at the yth row from the top and the xth
    character from the left in that row, given the rows in str_list
    and returns the new formatted string buffer list

    REQUIRES: X and Y are valid coordinates in the str_list
    e.g. X, Y actually in  str_list and not outside
    """
    s = str_list[y]
    l_s = len(s)

    s_new = s[0: x] + str(c) + s[x: l_s]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return new_str_list


def delete(x, y, str_list):
    """
    delete(x, y, str_list) deletes the character at the yth row from the top and the xth
    character from the left in that row, given the rows in str_list
    and returns the new formatted string buffer list.

    If str_list is empty, will act as NOP, no action

    REQUIRES: X and Y are valid coordinates in the str_list
    e.g. X, Y actually in  str_list and not outside
    """
    if str_list == []:
        return str_list

    s = str_list[y]
    s_new = s[0: x] + s[(x + 1):]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return new_str_list


class Screen:
    """
    Screen is an object representing the editing screen.
    str_list is the list of string buffers
    camera_level is the row in the str_list that marks the top of the editing
        box
    h is the height of the screen [h >= 0]
    w is the width of the screen [w >= 0]
    ulx is upper left x coordinate
    uly is upper left y coordinate
    cursor is a tuple containing an x - y pair of where the mouse
    is in:
    w > Cursor.x >= 0
    and
    h > Cursor.y >= 0
    Can only animate portion of camera from camera_level to
    camera_level + h - 1, inclusive of both first and last lines

    If the buffer list becomes empty, replace it with an empty string 
    automatically

    IMPORTANT: the screen y coordinate is always between camera_level
        and camera_level  + h  - 1 inclusive

    TO BE USED IN A STRUCT MANNER

    DIRECTION: X increases left yo right
    Y increases top down

    DISPLAY:
    """

    def __init__(self, str_list, h=Constants.NROWS, w=Constants.NCOLS, ulx=0, uly=0, cursor=(0, 0)):
        """
        Initializes a screen object for use as a struct

        DIRECTION: X increases left yo right
        Y increases top down
        """
        self.buffer = str_list
        self.h = h
        self.w = w
        self.ulx = ulx - ulx
        self.uly = uly - uly
        self.cursor = (0, 0)  # (ulx, uly)  # cursor = (0, 0)??
        self.screen_cursor = (0, 0)  # (ulx, uly)
        self.camera_level = 0  # uly

    def update_screen(self, op, c):
        """
        update_screen(self, op) updates the screen based on op,
        which is the ascii code for the key pressed
        c is the corresponding character

        e.g. Backspace or BS is ascii 08
        """
        # check not empty character
        if self.buffer == []:
            self.buffer = [Constants.EDITOR_START_CHAR]
        # update cursor
        if op == Constants.UP:
            self.scroll_up()
        elif op == Constants.DOWN:
            self.scroll_down()
        elif op == Constants.RIGHT:
            self.scroll_right()
        elif op == Constants.LEFT:
            self.scroll_left()
        elif op == Constants.DELETE:
            x, y = self.cursor
            str_list = self.buffer
            new_str_list = delete(x, y, str_list)
            # move x key back one if possible
            if x != 0:
                self.cursor = (max(x - 1, 0), y)
            # otherwise push key up a row
            elif y != 0:
                buffer = str_list[y - 1]
                l = len(buffer)
                self.cursor = (l - 1, y - 1)
            else:
                self.cursor = (0, max(y - 1, 0))
            self.buffer = new_str_list
        # insert newline/carriage return
        elif op == Constants.RETURN:
            x, y = self.cursor
            str_list = self.buffer
            new_str_list = insert("\n", x, y, str_list)
            # buffer = new_str_list[y]
            # l = len(buffer)
            # if y == (l - 1):
            #     # rule - insert space after a newline so can access
            #     new_str_list = new_str_list + [" "]
            self.cursor = (x, y)
            self.buffer = new_str_list
        # character update
        else:
            x, y = self.cursor
            str_list = self.buffer
            new_str_list = insert(c, x, y, str_list)
            num_rows = len(new_str_list)
            buffer = new_str_list[y]
            l = len(buffer)
            if x < (l - 1):
                self.cursor = (x + 1, y)
            elif y < (num_rows - 1):
                self.cursor = (0, y + 1)
            else:
                self.cursor = (x, y)
            self.buffer = new_str_list

        # update camera
        # self.change_camera()

        # update screen cursor
        self.change_screen_cursor()

    def change_screen_cursor(self):
        """
        change_screen_cursor(self) converts the cursor x y coordinate
        to a screen display x y coordinate

        E.g. the y coordinate is always between camera_level
        and camera_level  + h  - 1 inclusive

        REQUIRES: MUST BE CALLED ONLY AFTER change_camera is called
        so that the y coordinate is in camera frame
        """
        x, y = self.cursor
        top = self.camera_level
        bottom = top + self.h - 1
        assert y >= top
        assert y <= bottom

        screen_y = y - top

        self.screen_cursor = (x, screen_y)

    def change_camera(self):
        """
        change_camera(self) makes the top of the editing screen
        the y coordinate of the cursor whenever the y_coordinate
        of the str_list cursor drops below the actual screen camera

        REQUIRES: Call change_camera after cursor was moved
        """
        _, y = self.cursor
        screen_top = self.camera_level
        screen_bottom = self.camera_level + self.h - 1

        # leave camera screen by scrolling up
        if y < screen_top:
            # never go up beyond actual top
            self.camera_level = max(self.camera_level - self.h, self.uly)
            return

        # leave camera sceeen by scrolling down
        if y > screen_bottom:
            # shift camera down
            self.camera_level = self.camera_level + self.h
            return

        # NOP
        return

    def scroll_up(self):
        """
        Decreases cursor y coordinate by 1 if possible (MOVES UP ONE ROW)
        NOP if the cursor y is at the top row (e.g. equal to 0)

        Updates self

        REQUIRES: the Y coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        x, y = self.cursor

        # top most row
        if y == 0:
            return

        buffer = self.buffer
        s = buffer[y - 1]
        l = len(s)

        # if x coordinate in current row is not existent in next row up
        if x >= l:
            self.cursor = (l - 1, y - 1)
            return

        # x coordinate exists in next row up
        self.cursor = (x, y - 1)

    def scroll_down(self):
        """
        Increases cursor y coordinate by 1 if possible (MOVES DOWN ONE ROW)
        NOP if there is no additional row of text below

        Updates self

        REQUIRES: the Y coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        x, y = self.cursor
        buffer = self.buffer
        l = len(buffer)

        if (y == l - 1):
            self.cursor = (x, y)
            # self.buffer.append(Constants.EDITOR_START_CHAR)
            return

        # if (y == l - 1) and (buffer[y] == " "):
        #     self.cursor = (0, y)
        #     return

        # if y > len(buffer) - 1:
        #     self.cursor = (x, y)
        #     return

        s = buffer[y + 1]
        l = len(s)

        # if x coordinate in current row is not existent in next row down
        if x >= l:
            self.cursor = (l - 1, y + 1)
            return

        # x coordinate exists in next row down
        self.cursor = (x, y + 1)

    def scroll_left(self):
        """
        Decreases cursor x coordinate by 1 if possible (MOVES LEFT ONE COLUMN)
        NOP if there is no additional COLUMN of text to the left
        NOP if at left column border

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        x, y = self.cursor

        # if x is at the left border nop
        if x == 0:
            return

        # update
        self.cursor = (x - 1, y)

    def scroll_right(self):
        """
        Increases cursor x coordinate by 1 if possible (MOVES RIGHT ONE COLUMN)
        NOP if there is no additional COLUMN of text to the right

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        OR if you are one element right of the buffer, but not at the border
        """
        if self.buffer == []:
            return

        x, y = self.cursor
        buffer = self.buffer
        s = buffer[y]
        l = len(s)
        # check no more characters to the right or right boundary reached
        if (x == Constants.LINE_LENGTH - 1):  # or x == (l - 1):
            return

        if (x == (l - 1)):

            # last character is a regular space:
            if s[l - 1] == " ":
                self.cursor = (x, y)
                return

            # last character is a new line
            if "\n" in s or "\r" in s:
                self.cursor = (x, y)
                return

            else:
                self.cursor = (x + 1, y)
                return

        if (x > (l - 1)):
            self.cursor = (x, y)
            return

        # update
        self.cursor = (x + 1, y)

    def scroll_top(self):
        """
        Decreases cursor y coordinate by to start of rows

        Updates self

        REQUIRES: the Y coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        x, _ = self.cursor

        buffer = self.buffer
        s = buffer[0]
        l = len(s)

        if x >= l:
            self.cursor = (l - 1, 0)
            return

        self.cursor = (x, 0)

    def scroll_bottom(self):
        if self.buffer == []:
            return

        x, _ = self.cursor

        buffer = self.buffer
        bottom = len(buffer) - 1
        s = buffer[bottom]
        l = len(s)

        if x >= l:
            self.cursor = (l - 1, bottom)
            return

        self.cursor = (x, bottom)

    def scroll_far_left(self):
        """
        Decreases cursor x coordinate by to start of column

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        _, y = self.cursor
        self.cursor = (0, y)

    def scroll_far_right(self):
        """
        Increases cursor x coordinate by to end of column

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        """
        if self.buffer == []:
            return

        _, y = self.cursor
        buffer = self.buffer
        s = buffer[y]
        l = len(s)
        self.cursor = (l - 1, y)


def print_buffer_to_textbox(stdscr, buffer, max_rows, max_cols, uly, ulx):
    stdscr.erase()
    original_uly = uly
    stdscr.move(uly, ulx)
    for i in range(min(max_rows, len(buffer))):
        stdscr.addstr(buffer[i])
        uly += 1
        stdscr.move(uly, ulx)

    uly = original_uly
    stdscr.move(uly, ulx)
    textpad.rectangle(stdscr, uly-1, ulx-1, uly +
                      max_rows + 2, ulx + max_cols + 2)


def view_textbox(stdscr, insert_mode=True):
    ncols, nlines = Constants.LINE_LENGTH, Constants.NUM_LINES
    uly, ulx = 2, 2

    text = "Hello World!"
    str_list = split_text(text)

    screen = Screen(str_list, nlines, ncols, ulx, uly, (0, 0))

    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines + 2, ulx + ncols + 2)
    stdscr.move(uly, ulx)
    stdscr.addstr(text)
    stdscr.move(uly, ulx)
    stdscr.refresh()

    while True:
        op = stdscr.getch()
        c = chr(op)

        try:
            screen.update_screen(op, c)
            x, y = screen.screen_cursor

            stdscr.move(uly, ulx)

            print_buffer_to_textbox(
                stdscr, screen.buffer, nlines, ncols, uly, ulx)

            stdscr.move(uly + y, ulx + x)

        except:
            traceback.print_exc()

        # if op == Constants.RIGHT:
        #     if ulx < ncols:
        #         ulx += 1
        #     stdscr.move(uly, ulx)
        # elif op == Constants.LEFT:
        #     if ulx > 0:
        #         ulx -= 1
        #     stdscr.move(uly, ulx)
        # elif op == Constants.UP:
        #     if uly > 0:
        #         uly -= 1
        #     stdscr.move(uly, ulx)
        # elif op == Constants.DOWN:
        #     if uly < nlines:
        #         uly += 1
        #     stdscr.move(uly, ulx)
        stdscr.refresh()

    # box = textpad.Textbox(win, insert_mode)

    # contents = box.edit()
    # stdscr.addstr(uly+ncols+2, 0, "Text entered in the box\n")
    # stdscr.addstr(repr(contents))
    # stdscr.addstr('\n')
    # stdscr.addstr('Press any key')
    # stdscr.getch()

    # for i in range(3):
    #     stdscr.move(uly+ncols+2 + i, 0)
    #     stdscr.clrtoeol()


def view():
    try:
        # -- Initialize --
        stdscr = curses.initscr()   # initialize curses screen

        curses.noecho()
        curses.cbreak()             # enter break mode where pressing Enter key
        stdscr.keypad(1)

        # -- Perform an action with Screen --

        view_textbox(stdscr, insert_mode=False)

        while True:
            # stay in this loop till the user presses 'q'
            ch = stdscr.getch()
            if ch == ord('q'):
                break

        # -- End of user code --

    except:
        traceback.print_exc()     # print trace back log of the error
    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":

    def test():
        l = split_text(
            "HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello")
        l = insert("K", 55, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("K", 0, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("K", 5, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("\n", 1, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("\r", 0, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("\r", 5, 0, l)
        print(l)

        l = split_text(
            "LOLOL")
        l = insert("\r", 2, 0, l)
        print(l)

        s = "HelloHelloHelloHelloHelloHelloHelloHelloHello"
        l = split_text(s)
        print(l)
        for i in range(len(s) - 1, -1, -1):
            l = delete(i, 0, l)
        print(l)

        s = "HelloHello\nHell\roHelloHelloHelloHelloHelloHello"
        l = split_text(s)
        l = delete(10, 0, l)
        print(l)
        l = delete(14, 0, l)
        print(l)

        l = split_at_newline("Hello\nReady to go \r LOLOL\r", [])
        print(l)
        l = split_at_newline("Hello\n \r ", [])
        print(l)
        l = split_at_newline("\r\r", [])
        print(l)
        l = split_at_newline("\r", [])
        print(l)
        l = split_at_newline("", [])
        print(l)
        l = split_at_newline("H", [])
        print(l)

        l = split_text("Hello\nReady to go \r LOLOL\r")
        print(l)
        l = split_text("Hello\n \r ")
        print(l)
        l = split_text("\r\r")
        print(l)
        l = split_text("\r")
        print(l)
        l = split_text("")
        print(l)
        l = split_text("H")
        print(l)

        l = split_text(
            "HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello")
        print(l)
        l = split_text(
            "HelloHelloHelloHello\nHelloHelloHelloHello\rHelloHelloHelloHelloHelloHelloHelloHelloHelloHello")
        print(l)
        l = split_text(
            "HelloHelloHelloHello\nHelloHelloHelloHello\r\nHelloHello\rHelloHelloHelloHelloHelloHelloHelloHello")
        print(l)

        l = join_text(l)
        print(l)

    test()

    view()
