import Constants

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
            elif (text[i] == "\n" or text[i] == "r"):
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


def join_text(str_list):
    """
    join_text(text) joins list of strings into a string of text

    PROPERTY: INverse of split_text
    """
    return "".join(str_list)


l = join_text(l)
print(l)


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
    return new_str_list


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
    return new_str_list


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


class Screen:
    """
    Screen is an object representing the editing screen.
    h is the height of the screen [h >= 0]
    w is the width of the screen [w >= 0]
    ulx is upper left x coordinate 
    uly is upper left y coordinate
    cursor is a tuple containing an x - y pair of where the mouse
    is in:
    w > Cursor.x >= 0
    and 
    h > Cursor.y >= 0

    TO BE USED IN A STRUCT MANNER
    """

    def __init__(self, h=Constants.NROWS, w=Constants.NCOLS, ulx=0, uly=0, cursor=(0, 0)):
        """
        Initializes a screen object for use as a struct
        """
        self.h = h
        self.w = w
        self.ulx = ulx
        self.uly = uly
        self.cursor = cursor
