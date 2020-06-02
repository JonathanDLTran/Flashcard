import Constants
import curses
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


def add_space_at_end(str_list):
    return str_list + [" "]


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
            elif (text[i] == "\n" or text[i] == "r"):
                first_half = text[0: (i + 1)]
                second_half = text[(i + 1): l]
                return split_text_helper(second_half, str_list + [first_half])
            i += 1

    return add_space_at_end(split_text_helper(text, []))


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
    """
    s = str_list[y]
    l_s = len(s)

    s_new = s[0: x] + str(c) + s[x: l_s]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return add_space_at_end(new_str_list)


def delete(x, y, str_list):
    """
    delete(x, y, str_list) deletes the character at the yth row from the top and the xth
    character from the left in that row, given the rows in str_list
    and returns the new formatted string buffer list.

    If str_list is empty, will act as NOP, no action

    REQUIRES: X and Y are valid coordinates in the str_list
    """
    if str_list == []:
        return str_list

    s = str_list[y]
    s_new = s[0: x] + s[(x + 1):]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return add_space_at_end(new_str_list)


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
        self.ulx = ulx
        self.uly = uly
        self.cursor = (ulx, uly)  # cursor = (0, 0)??
        self.screen_cursor = (ulx, uly)
        self.camera_level = uly

    def update_screen(self, op, c):
        """
        update_screen(self, op) updates the screen based on op,
        wjich is the ascii code for the key pressed
        c is the corresponding character

        e.g. Backspace or BS is ascii 08
        """
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
            else:
                self.cursor = (0, max(y - 1, 0))
            self.buffer = new_str_list
        # insert newline/carriage return
        elif op == Constants.NEXTLINE:
            x, y = self.cursor
            str_list = self.buffer
            new_str_list = insert("\n", x, y, str_list)
            self.cursor = (x, y)
            self.buffer = new_str_list
        # character update
        else:
            x, y = self.cursor
            str_list = self.buffer
            new_str_list = insert("\n", x, y, str_list)
            self.cursor = (x, y)
            self.buffer = new_str_list

        # update camera
        self.change_camera

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
        _, y = self.cursor
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

        if y == len(buffer) - 1:
            return

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
        """
        if self.buffer == []:
            return

        x, y = self.cursor
        buffer = self.buffer
        s = buffer[y]
        l = len(s)
        # check no more characters to the right or right boundary reached
        if (x == Constants.LINE_LENGTH - 1) or x == (l - 1):
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


def view():
    pass


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
