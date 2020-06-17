import Constants
import curses
from curses import ascii
import traceback
from curses import textpad
import math
import functools
import json
import copy

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


def strike(text):
    """
    ASCII strikethrough, found on stack overflow from some nice guys over there
    # https://stackoverflow.com/questions/25244454/
    # python-create-strikethrough-strikeout-overstrike-string-type
    """
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


def find(word, chars):
    if word == "":
        remove_find_color()
        return
    match_locs = find_match(word, chars)
    change_find_color()
    return


def change_find_color():
    pass


def remove_find_color():
    pass


def find_match(word, chars):
    """
    Returns a list of positions where word matches chars, if no  amtches then 
    empty list reutnred

    REQUIRES: word is a string and has length >= 1 and chars is a list
    """
    matches = []
    w = word[0]
    for i in range(len(chars)):
        c = chars[i]
        if w == c:
            res = check_match(word, chars, i)
            if res:
                matches.append(i)
    return matches


def check_match(word, chars, i):
    """
    check_match(word, chars, i) checks that word completely matches
    the characters at chars[i,...len(word) - 1 + i] and returns true
    otherwise if no match than false. 
    RequirsL i in chars e.g, i < len(chars) and word[0] == chars[i]
    Word need not be in chars and can be longer than chars or extend
    pass chars end
    """
    if len(word) > len(chars[i:]):
        return False
    for j in range(1, len(word)):
        if word[j] != chars[i + j]:
            return False
    return True


def init_buffer(string):
    """
    initializes a buffer based on the string
    """
    return split_text(add_style(clean_text(string)))


def buffer_is_empty(buffer):
    return buffer == []


def clean_text(string):
    """
    clean_text(string) replaces tabs with appropriate number of spaces not going
    over column limit using TAB_SIZE as defined

    Returns new string with tabs removed and replaced appropriately

    REQUIRES: TAB SIZE <= LINE LENGTH
    """
    counter = 0
    new_string = ""
    for c in string:
        if c == "\n" or c == "\r":
            new_string += c
            counter = 0
        elif c == "\t" and counter + Constants.TAB_SIZE - 1 > Constants.LINE_LENGTH - 1:
            # tab replaced with as many spaces as possible before hitting right bound
            new_string += (Constants.LINE_LENGTH - counter) * " "
            counter = 0
        elif counter == Constants.LINE_LENGTH - 1:
            new_string += c
            counter = 0
        elif c == "\t":
            rem = Constants.TAB_SIZE - counter % Constants.TAB_SIZE
            new_string += rem * " "
            counter += rem
        else:
            new_string += c
            counter += 1
    return new_string


def add_style(string):
    """
    add_style(str) turns str into a list of lists with style inserted
    """
    final_split = []
    for c in string:
        final_split.append([c, curses.A_NORMAL])
    return final_split


def remove_style(style_list):
    """
    remove_style(style_list) restores the style list to a string
    """
    s = ""
    for l in style_list:
        s += l[0]
    return s


def buffer_repr(buffer):
    """
    buffer_repr(buffer) converts the buffer to a list - string represrntation
    """
    new_list = []
    for l in buffer:
        new_list.append(remove_style(l))
    return new_list


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
            elif (text[i][0] == "\n" or text[i][0] == "\r"):
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
    if text == []:
        return str_list

    l = len(text)
    i = 0
    while (i < l):
        if (text[i][0] == "\n") or (text[i][0] == "\r"):
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
    new_list = []
    for l in str_list:
        new_list += l
    return new_list


def insert(c, x, y, str_list):
    """
    insert(c, x, y, str_list) inserts a character c at the yth row from the top and the xth
    character from the left in that row, given the rows in str_list
    and returns the new formatted string buffer list

    REQUIRES: X and Y are valid coordinates in the str_list
    e.g. X, Y actually in str_list and not outside
    """
    s = str_list[y]
    l_s = len(s)

    s_new = s[0: x] + [c] + s[x: l_s]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return new_str_list


def retrieve_text(x1, y1, x2, y2, str_list):
    """
    retrieve_text(x1, y1, x2, y2, str_list)
    retrieves the strings of text from str_list bounded from
    x1, y1 to x2, y2. Returns a string inclusive of x1 AND x2
    that is includes both ending locations

    USE: FOR COPY AND CUT

    REQUORES: x1, y1 must come sequentially after x2, yx2
    REQUIRES: x1 and x2 are valid locations in str_list
    """
    assert (x1 <= x2 and y1 == y2) or (y1 < y2)

    def retrieve_text_helper(x1, y1, x2, y2, str_list, acc):
        # same line (one line)
        if (y1 == y2):
            buffer = str_list[y1]
            s = buffer[x1: (x2 + 1)]
            return acc + [s]

        # two or more lines
        first_line = str_list[y1]
        l = len(first_line)
        s = first_line[x1: l]
        return retrieve_text_helper(0, (y1 + 1), x2, y2, str_list, acc + [s])

    return join_text(retrieve_text_helper(x1, y1, x2, y2, str_list, []))


def bulk_insert(s, x, y, str_list):
    """
    bulk_insert(s, x, y, str_list) adds in all characters in s beginning
    at x, y in str_list

    Returns modified str_list after all bulk insertion is complete

    USe: Copy/Cut
    """
    s_rev = s[::-1]
    for i in range(len(s_rev)):
        c = s_rev[i]
        str_list = insert(c, x, y, str_list)
    return str_list


def delete(x, y, str_list):
    """
    delete(x, y, str_list) deletes the character at the yth row from the top and the xth
    character from the left in that row, given the rows in str_list
    and returns the new formatted string buffer list.

    If str_list is empty, will act as NOP, no action

    REQUIRES: X and Y are valid coordinates in the str_list
    e.g. X, Y actually in str_list and not outside
    """
    if str_list == []:
        return str_list

    s = str_list[y]
    s_new = s[0: x] + s[(x + 1):]
    str_list[y] = s_new

    new_text = join_text(str_list)
    new_str_list = split_text(new_text)
    return new_str_list


def bulk_delete(s, x, y, str_list):
    """
    bulk_delete(s, x, y, str_list) removes all characters in s beginning
    at x, y in str_list

    Returns the modified str_list after the bulk_delete has finished

    Use: Cut
    """
    for _ in range(len(s)):
        str_list = delete(x, y, str_list)
    return str_list


def buffer_add_row(buffer, y, c):
    buffer[y] += [[c, curses.A_NORMAL]]
    return buffer


def get_max_min(x1, y1, x2, y2):
    """
    get_max_min(x1, y1, x2, y2) returns two tuples,
    such that the first tuple has either y1 == y2 and x1 <= x2
    or y1 < y2
    """
    if y1 == y2:
        tempx1 = x1
        tempx2 = x2
        x1 = min(tempx1, tempx2)
        x2 = max(tempx1, tempx2)
    elif y1 > y2:
        tempx, tempy = x1, y1
        x1, y1 = x2, y2
        x2, y2 = tempx, tempy
    return ((x1, y1), (x2, y2))


def insert_style_buffer(start_tup, end_tup, buffer, style):
    x1, y1 = start_tup
    x2, y2 = end_tup

    if y1 == y2:
        row = buffer[y1]
        for i in list(range(x1, (x2 + 1), 1)):
            c_list = row[i]
            if style in c_list:
                c_list.remove(style)
            else:
                c_list.append(style)
        return buffer

    else:
        row = buffer[y1]
        l = len(row)
        for i in list(range(x1, l, 1)):
            c_list = row[i]
            if style in c_list:
                c_list.remove(style)
            else:
                c_list.append(style)

        next_tup = (0, y1 + 1)
        return insert_style_buffer(
            next_tup, end_tup, buffer, style)


def insert_color_buffer(start_tup, end_tup, buffer, color):
    x1, y1 = start_tup
    x2, y2 = end_tup

    if y1 == y2:
        row = buffer[y1]
        for i in list(range(x1, (x2 + 1), 1)):
            c_list = row[i]
            # 1 index is color
            c_list[1] = color
        return buffer

    else:
        row = buffer[y1]
        l = len(row)
        for i in list(range(x1, l, 1)):
            c_list = row[i]
            # 1 index is color
            c_list[1] = color

        next_tup = (0, y1 + 1)
        return insert_style_buffer(
            next_tup, end_tup, buffer, color)


def legal_macro_commands(op):
    if op == Constants.UP:
        return False
    elif op == Constants.DOWN:
        return False
    elif op == Constants.RIGHT:
        return False
    elif op == Constants.LEFT:
        return False
    elif op == Constants.GO_RIGHT:
        return False
    elif op == Constants.GO_LEFT:
        return False
    elif op == Constants.GO_TOP:
        return False
    elif op == Constants.GO_BOTTOM:
        return False
    elif op == Constants.UP_ONE_PAGE:
        return False
    elif op == Constants.DOWN_ONE_PAGE:
        return False

    elif op == Constants.UNDO:
        return False
    elif op == Constants.REDO:
        return False

    elif op == Constants.BOLD:
        return False
    elif op == Constants.HIGHLIGHT:
        return False
    elif op == Constants.UNDERLINE:
        return False

    elif op == Constants.EXIT_EDITOR:
        return False

    elif op == Constants.MACRO_RECORD:
        return False
    elif op == Constants.MACRO_RUN:
        return False

    # colors
    elif op == Constants.COLOR_BLACK:
        return False
    elif op == Constants.COLOR_CYAN:
        return False
    elif op == Constants.COLOR_GREEN:
        return False
    elif op == Constants.COLOR_YELLOW:
        return False
    elif op == Constants.COLOR_RED:
        return False

    elif op == Constants.COPY:
        return False
    elif op == Constants.CUT:
        return False
    elif op == Constants.PASTE:
        return False

    elif op == Constants.ESCAPE:
        return False

    elif op == Constants.COPY_ALL:
        return False

    elif op == Constants.SETB1:
        return False
    elif op == Constants.SETB2:
        return False
    elif op == Constants.SETB3:
        return False
    elif op == Constants.SETB4:
        return False
    elif op == Constants.SETB5:
        return False

    elif op == Constants.JUMPB1:
        return False
    elif op == Constants.JUMPB2:
        return False
    elif op == Constants.JUMPB3:
        return False
    elif op == Constants.JUMPB4:
        return False
    elif op == Constants.JUMPB5:
        return False

    return True


class Screen:
    """
    Screen is an object representing the editing screen.
    str_list is the list of string buffers
    camera_level is the row in the str_list that marks the top of the editing
        box
    h is the height of the screen[h >= 0]
    w is the width of the screen[w >= 0]
    ulx is upper left x coordinate
    uly is upper left y coordinate
    cursor is a tuple containing an x - y pair of where the mouse
    is in:
    w > Cursor.x >= 0
    and
    h > Cursor.y >= 0
    Can only animate portion of camera from camera_level to
    camera_level + h - 1, inclusive of both first and last lines

    copy_loc2 cannot be anothing but None None if copy_loc1 is None None

    If the buffer list becomes empty, replace it with an empty string
    automatically

    IMPORTANT: the screen y coordinate is always between camera_level
        and camera_level + h - 1 inclusive

    TO BE USED IN A STRUCT MANNER

    DIRECTION: X increases left yo right
    Y increases top down

    DISPLAY:
    """

    def __init__(self, string, h=Constants.NROWS, w=Constants.NCOLS, ulx=0, uly=0, cursor=(0, 0)):
        """
        Initializes a screen object for use as a struct

        DIRECTION: X increases left yo right
        Y increases top down
        """
        self.buffer = init_buffer(string)
        self.h = h
        self.w = w
        self.ulx = 0
        self.uly = 0
        self.cursor = (0, 0)  # (ulx, uly)  # cursor = (0, 0)??
        self.screen_cursor = (0, 0)  # (ulx, uly)
        self.camera_level = 0  # uly

        self.bookmarks = Constants.NUM_BOOKMARKS * [None]

        self.copy_loc1 = (None, None)
        self.copy_loc2 = (None, None)

        self.cut_loc1 = (None, None)
        self.cut_loc2 = (None, None)

        self.copy_buffer = None

        self.exit_editor = False

        self.bold_loc1 = (None, None)
        self.bold_loc2 = (None, None)

        self.highlight1 = (None, None)
        self.highlight2 = (None, None)

        self.underline1 = (None, None)
        self.underline2 = (None, None)

        self.copy_all = None

        self.color1 = (None, None)
        self.color2 = (None, None)

        self.color = None

        self.save_pointer = 0
        self.save_buffer = [copy.deepcopy(self.buffer)]
        self.saved_cursor = [copy.deepcopy(self.cursor)]

        self.redo_pointer = 0
        self.redo_buffer = [copy.deepcopy(self.buffer)]
        self.redo_cursor = [copy.deepcopy(self.cursor)]

        self.macro_buffer = []
        self.start_macro = False

    def update_edit_history(self, undo_occurred):
        if undo_occurred:
            return
        self.save_pointer += 1
        self.save_buffer += [copy.deepcopy(self.buffer)]
        self.saved_cursor += [copy.deepcopy(self.cursor)]
        if self.save_pointer >= Constants.SAVE_TRACK_LENGTH:
            diff = self.save_pointer - Constants.SAVE_TRACK_LENGTH + 1
            self.save_buffer = self.save_buffer[diff:]
            self.saved_cursor = self.saved_cursor[diff:]
            self.save_pointer -= diff

        # at every update, the redo buffer is updated as well
        self.redo_pointer = 0
        self.redo_buffer = [copy.deepcopy(self.buffer)]
        self.redo_cursor = [copy.deepcopy(self.cursor)]

    def update_undo(self):
        # reset redo
        self.add_redo(self.buffer, self.cursor)

        # if no edits made on current line, no op
        if self.save_pointer == 0:
            self.buffer = self.save_buffer[self.save_pointer]
            # move cursor
            self.cursor = self.saved_cursor[self.save_pointer]

            self.save_buffer = [copy.deepcopy(self.buffer)]
            self.saved_cursor = [copy.deepcopy(self.cursor)]
            return

        self.save_pointer -= 1
        self.buffer = self.save_buffer[self.save_pointer]
        # move cursor
        self.cursor = self.saved_cursor[self.save_pointer]

        # update saved buffer
        l = len(self.save_buffer)
        self.save_buffer = self.save_buffer[:(l - 1)]
        # update saved cursor
        self.saved_cursor = self.saved_cursor[:(l - 1)]

    def flush_undo(self, buffer, cursor):
        self.save_pointer = 0
        self.saved_cursor = [copy.deepcopy(cursor)]
        self.save_buffer = [copy.deepcopy(buffer)]

    def add_redo(self, buffer, cursor):
        self.redo_pointer += 1
        self.redo_cursor += [copy.deepcopy(cursor)]
        self.redo_buffer += [copy.deepcopy(buffer)]

        if self.redo_pointer >= Constants.SAVE_TRACK_LENGTH:
            diff = self.redo_pointer - Constants.SAVE_TRACK_LENGTH + 1
            self.redo_buffer = self.redo_buffer[diff:]
            self.redo_cursor = self.redo_cursor[diff:]
            self.redo_pointer -= diff

    def update_redo(self):
        # once a redo occurs, undo is cleared
        self.flush_undo(self.buffer, self.cursor)

        # if no edits made on current line, no op
        if self.redo_pointer == 0:
            self.buffer = self.redo_buffer[self.redo_pointer]
            # move cursor
            self.cursor = self.redo_cursor[self.redo_pointer]

            self.redo_buffer = [copy.deepcopy(self.buffer)]
            self.redo_cursor = [copy.deepcopy(self.cursor)]
            return

        self.redo_pointer -= 1
        self.buffer = self.redo_buffer[self.redo_pointer]
        # move cursor
        self.cursor = self.redo_cursor[self.redo_pointer]

        # update saved buffer
        l = len(self.redo_buffer)
        self.redo_buffer = self.redo_buffer[:(l - 1)]
        # update saved cursor
        self.redo_cursor = self.redo_cursor[:(l - 1)]

    def reset_cut_copy(self):
        """
        reset_cut_copy(self) resets all stores and buffers when copyiny
        or cutting is terminated/escaped
        """
        self.reset_paste()

        self.copy_buffer = None

        self.copy_all = None

    def reset_paste(self):
        """
        reset_copy_paste(self) resets all cut locations
        """
        self.copy_loc1 = (None, None)
        self.copy_loc2 = (None, None)

        self.cut_loc1 = (None, None)
        self.cut_loc2 = (None, None)

    def update_cut(self):
        x, y = self.cursor
        if self.cut_loc1 == (None, None):
            self.cut_loc1 = (x, y)
            return
        else:
            self.cut_loc2 = (x, y)

        if self.cut_loc2 != (None, None):
            x1, y1 = self.cut_loc1
            x2, y2 = self.cut_loc2
            if y1 == y2:
                tempx1 = x1
                tempx2 = x2
                x1 = min(tempx1, tempx2)
                x2 = max(tempx1, tempx2)
            elif y1 > y2:
                tempx, tempy = x1, y1
                x1, y1 = x2, y2
                x2, y2 = tempx, tempy

            buffer = self.buffer
            l_buff = len(buffer)
            if y1 >= l_buff or y2 >= l_buff:
                self.reset_paste()
                return
            s1 = buffer[y1]
            s2 = buffer[y2]
            l_1 = len(s1)
            l_2 = len(s2)
            if x1 >= l_1 or x2 >= l_2:
                self.reset_paste()
                return

            last_length = len(self.buffer[y2])
            s = retrieve_text(x1, y1, x2, y2, self.buffer)
            self.copy_buffer = s
            self.buffer = bulk_delete(s, x1, y1, self.buffer)

            self.reset_paste()

            # move to beginning of cut
            if x1 != 0:
                self.cursor = (x1 - 1, y1)

                if x2 == last_length - 1:
                    self.buffer = buffer_add_row(self.buffer, y1, "\n")

            elif x1 == 0 and y1 == 0:
                self.cursor = (0, 0)

            else:
                buffer = self.buffer
                s = buffer[y1 - 1]
                l = len(s)
                self.cursor = (l - 1, y1 - 1)

                if x2 == last_length - 1:
                    self.buffer = buffer_add_row(self.buffer, y1 - 1, "\n")

    def update_copy(self):
        x, y = self.cursor
        if self.copy_loc1 == (None, None):
            self.copy_loc1 = (x, y)
        else:
            self.copy_loc2 = (x, y)

        if self.copy_loc2 != (None, None):
            x1, y1 = self.copy_loc1
            x2, y2 = self.copy_loc2
            if y1 == y2:
                tempx1 = x1
                tempx2 = x2
                x1 = min(tempx1, tempx2)
                x2 = max(tempx1, tempx2)
            elif y1 > y2:
                tempx, tempy = x1, y1
                x1, y1 = x2, y2
                x2, y2 = tempx, tempy

            buffer = self.buffer
            l_buff = len(buffer)
            if y1 >= l_buff or y2 >= l_buff:
                self.reset_paste()
                return
            s1 = buffer[y1]
            s2 = buffer[y2]
            l_1 = len(s1)
            l_2 = len(s2)
            if x1 >= l_1 or x2 >= l_2:
                self.reset_paste()
                return

            self.copy_buffer = retrieve_text(
                x1, y1, x2, y2, self.buffer)

    def update_paste(self):
        s = self.copy_buffer
        if s != None:
            x, y = self.cursor
            self.buffer = bulk_insert(s, x, y, self.buffer)
            self.reset_paste()
            return

    def update_delete(self):
        """
        update_delete(self) updates the cursor and buffer after
        a character is deleted where the cursor was

        Requires: cursor lies on a character
        """
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

    def update_return(self):
        """
        update_return(self) adds in a newline where the cursor is

        Requires: cursor lies on a character
        """
        x, y = self.cursor
        str_list = self.buffer
        new_str_list = insert(["\n", curses.A_NORMAL], x, y, str_list)
        # buffer = new_str_list[y]
        # l = len(buffer)
        # if y == (l - 1):
        #     # rule - insert space after a newline so can access
        #     new_str_list = new_str_list + [" "]

        # TRY NEW
        # self.cursor = (x, y)
        # TRY NEW
        self.cursor = (0, y + 1)
        self.buffer = new_str_list

    def update_insert(self, c):
        """
        update_insert(self) adds in a new character where the cursor is
        and maintains invariant aftr

        Requires: cursor lies on a character
        """
        x, y = self.cursor
        str_list = self.buffer
        new_str_list = insert([c, curses.A_NORMAL], x, y, str_list)
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

    def jump_to_bookmark(self, bookmark_n):
        """
        jump_to_bookmark(self, bookmark_n) jumps cursor to book mark n
        n is between 1 and 5 inclusive
        """
        y = self.bookmarks[bookmark_n - 1]
        buffer = self.buffer
        l = len(buffer)
        if y == None:
            return
        if y >= l:
            return
        x, _ = self.cursor
        self.cursor = (x, y)

    def set_bookmark(self, bookmark_n):
        """
        set_bookmark(self, bookmark_n sets book mark n
        at the current cursor line location
        n is between 1 and 5 inclusive
        """
        self.bookmarks[bookmark_n - 1] = self.cursor[1]

    def update_quit(self):
        self.exit_editor = True

    def update_bold(self):
        """
        update_bold(self) either marks the beginning of the bolding or
        ends the bolding
        """
        x, y = self.cursor
        if self.bold_loc1 == (None, None):
            self.bold_loc1 = (x, y)
            return
        else:
            self.bold_loc2 = (x, y)

        # check both lie in buffer
        x1, y1 = self.bold_loc1
        x2, y2 = self.bold_loc2

        buffer = self.buffer
        l_buff = len(buffer)
        if y1 >= l_buff or y2 >= l_buff:
            self.bold_loc1 = (None, None)
            self.bold_loc2 = (None, None)
            return
        s1 = buffer[y1]
        s2 = buffer[y2]
        l_1 = len(s1)
        l_2 = len(s2)
        if x1 >= l_1 or x2 >= l_2:
            self.bold_loc1 = (None, None)
            self.bold_loc2 = (None, None)
            return

        # update the bold buffer

        start_tup, end_tup = get_max_min(x1, y1, x2, y2)
        self.buffer = insert_style_buffer(
            start_tup, end_tup, self.buffer, curses.A_BOLD)

        # release bold loc 1 and 2
        self.bold_loc1 = (None, None)
        self.bold_loc2 = (None, None)

    def update_highlight(self):
        """
        update_bold(self) either marks the beginning of the bolding or
        ends the bolding
        """
        x, y = self.cursor
        if self.highlight1 == (None, None):
            self.highlight1 = (x, y)
            return
        else:
            self.highlight2 = (x, y)

        # check both lie in buffer
        x1, y1 = self.highlight1
        x2, y2 = self.highlight2

        buffer = self.buffer
        l_buff = len(buffer)
        if y1 >= l_buff or y2 >= l_buff:
            self.highlight1 = (None, None)
            self.highlight2 = (None, None)
            return
        s1 = buffer[y1]
        s2 = buffer[y2]
        l_1 = len(s1)
        l_2 = len(s2)
        if x1 >= l_1 or x2 >= l_2:
            self.highlight1 = (None, None)
            self.highlight2 = (None, None)
            return

        # update the bold buffer

        start_tup, end_tup = get_max_min(x1, y1, x2, y2)
        self.buffer = insert_style_buffer(
            start_tup, end_tup, self.buffer, curses.A_STANDOUT)

        # release bold loc 1 and 2
        self.highlight1 = (None, None)
        self.highlight2 = (None, None)

    def update_underline(self):
        """
        update_bold(self) either marks the beginning of the bolding or
        ends the bolding
        """
        x, y = self.cursor
        if self.underline1 == (None, None):
            self.underline1 = (x, y)
            return
        else:
            self.underline2 = (x, y)

        # check both lie in buffer
        x1, y1 = self.underline1
        x2, y2 = self.underline2

        buffer = self.buffer
        l_buff = len(buffer)
        if y1 >= l_buff or y2 >= l_buff:
            self.underline1 = (None, None)
            self.underline2 = (None, None)
            return
        s1 = buffer[y1]
        s2 = buffer[y2]
        l_1 = len(s1)
        l_2 = len(s2)
        if x1 >= l_1 or x2 >= l_2:
            self.underline1 = (None, None)
            self.underline2 = (None, None)
            return

        # update the bold buffer

        start_tup, end_tup = get_max_min(x1, y1, x2, y2)
        self.buffer = insert_style_buffer(
            start_tup, end_tup, self.buffer, curses.A_UNDERLINE)

        # release bold loc 1 and 2
        self.underline1 = (None, None)
        self.underline2 = (None, None)

    def update_color(self, color):
        x, y = self.cursor
        if self.color1 == (None, None):
            self.color1 = (x, y)
            self.color = color
            return
        elif self.color1 != (None, None) and self.color != color:
            self.color1 = (None, None)
            self.color = None
            return
        else:
            self.color2 = (x, y)
            self.color = None

        # check both lie in buffer
        x1, y1 = self.color1
        x2, y2 = self.color2

        buffer = self.buffer
        l_buff = len(buffer)
        if y1 >= l_buff or y2 >= l_buff:
            self.color1 = (None, None)
            self.color2 = (None, None)
            return
        s1 = buffer[y1]
        s2 = buffer[y2]
        l_1 = len(s1)
        l_2 = len(s2)
        if x1 >= l_1 or x2 >= l_2:
            self.color1 = (None, None)
            self.color2 = (None, None)
            return

        # update the bold buffer

        start_tup, end_tup = get_max_min(x1, y1, x2, y2)
        self.buffer = insert_color_buffer(
            start_tup, end_tup, self.buffer, color)

        # release bold loc 1 and 2
        self.color1 = (None, None)
        self.color2 = (None, None)

    def update_copy_all(self):
        if self.copy_all == None:
            buffer = self.buffer
            l = len(buffer)
            last_row = buffer[l - 1]
            l_last = len(last_row)
            self.copy_all = retrieve_text(0, 0, l_last - 1, l - 1, buffer)
            return
        else:
            x, y = self.cursor
            self.buffer = bulk_insert(self.copy_all, x, y, self.buffer)
            self.copy_all = None
            return

    def update_tab(self):
        x, y = self.cursor

        # within left boundary
        num_spaces = Constants.TAB_SIZE
        if (x + Constants.TAB_SIZE - 1) > Constants.LINE_LENGTH - 1:
            num_spaces = (Constants.LINE_LENGTH - x)
        else:
            num_spaces = Constants.TAB_SIZE - (x % Constants.TAB_SIZE)

        s = [[" ", curses.A_NORMAL] for _ in range(num_spaces)]
        self.buffer = bulk_insert(s, x, y, self.buffer)

        # update tab location
        self.cursor = (x + num_spaces, y)

    def update_save(self, json_path):
        fp = open(json_path, "w")
        json.dump(self.buffer, fp)
        fp.close()

    def update_record_macro(self):
        if not self.start_macro:
            self.macro_buffer = []
            self.start_macro = True
            return
        self.start_macro = False

    def update_macro_history(self, op):
        if self.start_macro:
            if legal_macro_commands(op):
                self.macro_buffer.append(op)
                return

    def update_run_macro(self, json_path):
        macro_history = self.macro_buffer
        for op in macro_history:
            self.update_screen(op, chr(op), json_path)

    def update_up_one_page(self):
        _, y = self.cursor
        self.cursor = (0, max(y - Constants.NUM_LINES, 0))

    def update_down_one_page(self):
        _, y = self.cursor
        l = len(self.buffer)
        self.cursor = (0, min(y + Constants.NUM_LINES, l - 1))

    def update_screen(self, op, c, json_path):
        """
        update_screen(self, op) updates the screen based on op,
        which is the ascii code for the key pressed
        c is the corresponding character

        e.g. Backspace or BS is ascii 08
        """
        # check not empty character
        if buffer_is_empty(self.buffer):
            self.buffer = init_buffer(Constants.EDITOR_START_CHAR)

        # update cursor
        if op == Constants.UP:
            self.scroll_up()
        elif op == Constants.DOWN:
            self.scroll_down()
        elif op == Constants.RIGHT:
            self.scroll_right()
        elif op == Constants.LEFT:
            self.scroll_left()
        elif op == Constants.GO_RIGHT:
            self.scroll_far_right()
        elif op == Constants.GO_LEFT:
            self.scroll_far_left()
        elif op == Constants.GO_TOP:
            self.scroll_top()
        elif op == Constants.GO_BOTTOM:
            self.scroll_bottom()
        elif op == Constants.UP_ONE_PAGE:
            self.update_up_one_page()
        elif op == Constants.DOWN_ONE_PAGE:
            self.update_down_one_page()

        elif op == Constants.TAB:
            self.update_tab()

        elif op == Constants.SAVE:
            self.update_save(json_path)
            return
        elif op == Constants.UNDO:
            self.update_undo()
        elif op == Constants.REDO:
            self.update_redo()

        elif op == Constants.BOLD:
            self.update_bold()
        elif op == Constants.HIGHLIGHT:
            self.update_highlight()
        elif op == Constants.UNDERLINE:
            self.update_underline()

        elif op == Constants.EXIT_EDITOR:
            self.update_quit()
            self.update_save(json_path)

        elif op == Constants.MACRO_RECORD:
            self.update_record_macro()
        elif op == Constants.MACRO_RUN:
            self.update_run_macro(json_path)

        # colors
        elif op == Constants.COLOR_BLACK:
            self.update_color(curses.A_NORMAL)
        elif op == Constants.COLOR_CYAN:
            self.update_color(curses.color_pair(5))
        elif op == Constants.COLOR_GREEN:
            self.update_color(curses.color_pair(6))
        elif op == Constants.COLOR_YELLOW:
            self.update_color(curses.color_pair(7))
        elif op == Constants.COLOR_RED:
            self.update_color(curses.color_pair(8))

        elif op == Constants.COPY:
            self.update_copy()
        elif op == Constants.CUT:
            self.update_cut()
        elif op == Constants.PASTE:
            self.update_paste()

        elif op == Constants.ESCAPE:
            self.reset_cut_copy()

        elif op == Constants.COPY_ALL:
            self.update_copy_all()

        elif op == Constants.SETB1:
            self.set_bookmark(1)
            return
        elif op == Constants.SETB2:
            self.set_bookmark(2)
            return
        elif op == Constants.SETB3:
            self.set_bookmark(3)
            return
        elif op == Constants.SETB4:
            self.set_bookmark(4)
            return
        elif op == Constants.SETB5:
            self.set_bookmark(5)
            return

        elif op == Constants.JUMPB1:
            self.jump_to_bookmark(1)
        elif op == Constants.JUMPB2:
            self.jump_to_bookmark(2)
        elif op == Constants.JUMPB3:
            self.jump_to_bookmark(3)
        elif op == Constants.JUMPB4:
            self.jump_to_bookmark(4)
        elif op == Constants.JUMPB5:
            self.jump_to_bookmark(5)

        elif op == Constants.DELETE:
            self.update_delete()
        # insert newline/carriage return
        elif op == Constants.RETURN:
            self.update_return()
        # character update
        else:
            self.update_insert(c)

        # update camera
        self.change_camera()

        # update screen cursor
        self.change_screen_cursor()

        # update macro buffer
        self.update_macro_history(op)

        # update edit history
        self.update_edit_history(op == Constants.UNDO or op == Constants.REDO)

    def change_screen_cursor(self):
        """
        change_screen_cursor(self) converts the cursor x y coordinate
        to a screen display x y coordinate

        E.g. the y coordinate is always between camera_level
        and camera_level + h - 1 inclusive

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
            mult = (screen_bottom - y) // self.h
            self.camera_level = max(
                self.camera_level - mult * self.h, self.uly)
            return

        # leave camera sceeen by scrolling down
        if y > screen_bottom:
            # shift camera down
            mult = (y - screen_top) // self.h
            self.camera_level = self.camera_level + mult * self.h
            return

        # NOP
        return

    def scroll_up(self):
        """
        Decreases cursor y coordinate by 1 if possible(MOVES UP ONE ROW)
        NOP if the cursor y is at the top row(e.g. equal to 0)

        Updates self

        REQUIRES: the Y coordinate was actually on a text element
        """
        if buffer_is_empty(self.buffer):
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
        Increases cursor y coordinate by 1 if possible(MOVES DOWN ONE ROW)
        NOP if there is no additional row of text below

        Updates self

        REQUIRES: the Y coordinate was actually on a text element
        """
        if buffer_is_empty(self.buffer):
            return

        x, y = self.cursor
        buffer = self.buffer
        l = len(buffer)

        if (y == l - 1):
            self.cursor = (x, y)
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
        Decreases cursor x coordinate by 1 if possible(MOVES LEFT ONE COLUMN)
        NOP if there is no additional COLUMN of text to the left
        NOP if at left column border

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        """
        if buffer_is_empty(self.buffer):
            return

        x, y = self.cursor

        # if x is at the left border nop
        if x == 0:
            return

        # update
        self.cursor = (x - 1, y)

    def scroll_right(self):
        """
        Increases cursor x coordinate by 1 if possible(MOVES RIGHT ONE COLUMN)
        NOP if there is no additional COLUMN of text to the right

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        OR if you are one element right of the buffer, but not at the border
        """
        if buffer_is_empty(self.buffer):
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
        if buffer_is_empty(self.buffer):
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
        if buffer_is_empty(self.buffer):
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
        if buffer_is_empty(self.buffer):
            return

        _, y = self.cursor
        self.cursor = (0, y)

    def scroll_far_right(self):
        """
        Increases cursor x coordinate by to end of column

        Updates self

        REQUIRES: the X coordinate was actually on a text element
        """
        if buffer_is_empty(self.buffer):
            return

        _, y = self.cursor
        buffer = self.buffer
        s = buffer[y]
        l = len(s)
        self.cursor = (l - 1, y)


def print_buffer_to_textbox(stdscr, camera_row, buffer, max_rows, max_cols, uly, ulx, x, y, screen):
    # regular text
    stdscr.erase()
    original_uly = uly
    original_ulx = ulx
    stdscr.move(uly, ulx)
    for i in range(camera_row, min(camera_row + max_rows, len(buffer))):
        row = buffer[i]
        for c_list in row:
            c = c_list[0]
            c_attr = functools.reduce(lambda a, acc: a | acc, c_list[1:])
            stdscr.addch(c, c_attr)

        uly += 1
        stdscr.move(uly, ulx)

    # redraw rectangle bounding box
    ulx = original_ulx
    uly = original_uly
    stdscr.move(uly, ulx)
    textpad.rectangle(stdscr, uly-1, ulx-1, uly +
                      max_rows + 2, ulx + max_cols + 2)

    # mode display
    stdscr.move(uly + max_rows + 3, ulx)
    stdscr.addstr("[Edit Mode]", curses.color_pair(1))

    # copy display
    stdscr.move(uly + max_rows + 3, ulx + 11)
    if screen.copy_loc2 != (None, None):
        stdscr.addstr("[Copied to Clipboard]", curses.color_pair(3))
    elif screen.copy_loc1 != (None, None):
        stdscr.addstr("[Copying... Give Next Location]", curses.color_pair(3))

    # cut display
    stdscr.move(uly + max_rows + 4, ulx + 11)
    if screen.cut_loc2 != (None, None):
        stdscr.addstr("[Cut onto Clipboard]", curses.color_pair(3))
    elif screen.cut_loc1 != (None, None):
        stdscr.addstr("[Cutting... Give Next Location]", curses.color_pair(3))

    # style display
    stdscr.move(uly + max_rows + 5, ulx + 11)
    if screen.bold_loc2 != (None, None):
        stdscr.addstr("[Bolded on Screen]", curses.color_pair(4))
    elif screen.bold_loc1 != (None, None):
        stdscr.addstr("[Bolding... Give Next Location]", curses.color_pair(4))

    stdscr.move(uly + max_rows + 6, ulx + 11)
    if screen.highlight2 != (None, None):
        stdscr.addstr("[Highlighted on Screen]", curses.color_pair(4))
    elif screen.highlight1 != (None, None):
        stdscr.addstr("[Highlighting... Give Next Location]",
                      curses.color_pair(4))

    stdscr.move(uly + max_rows + 7, ulx + 11)
    if screen.underline2 != (None, None):
        stdscr.addstr("[Underlined on Screen]", curses.color_pair(4))
    elif screen.underline1 != (None, None):
        stdscr.addstr("[Underlining... Give Next Location]",
                      curses.color_pair(4))

    # color display
    stdscr.move(uly + max_rows + 8, ulx + 11)
    if screen.color2 != (None, None):
        stdscr.addstr("[Color on Screen]", curses.color_pair(9))
    elif screen.color1 != (None, None):
        stdscr.addstr("[Coloring... Give Next Location]",
                      curses.color_pair(9))

    # copy all
    stdscr.move(uly + max_rows + 8, ulx + 11)
    if screen.copy_all != None:
        stdscr.addstr("[Copied All Text to Clipboard]", curses.color_pair(3))

    # macro recording
    stdscr.move(uly + max_rows + 9, ulx + 11)
    if screen.start_macro:
        stdscr.addstr("[Recording Macro]", curses.color_pair(10))

    # row column display
    num_digits = len(str(y + 1))
    stdscr.move(uly + max_rows + 3, ulx +
                max_cols + 2 - num_digits - 1 - 4 - 5)
    stdscr.addstr("Row " + str(y + 1), curses.color_pair(2))
    stdscr.move(uly + max_rows + 3, ulx + max_cols + 2 - 5)
    stdscr.addstr("Col " + str(x + 1), curses.color_pair(2))

    # page number display
    pages = (y + 1) // max_rows + 1
    page_digits = len(str(pages))
    stdscr.move(uly + max_rows + 4, ulx + max_cols + 2 - 4 - page_digits)
    stdscr.addstr("Page " + str(pages), curses.color_pair(2))

    stdscr.move(uly, ulx)


def view_textbox(stdscr, json_path, insert_mode=True):
    ncols, nlines = Constants.LINE_LENGTH, Constants.NUM_LINES
    uly, ulx = 2, 2

    text = "Hello World!\n"

    screen = Screen(text, nlines, ncols, ulx, uly, (0, 0))

    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines + 2, ulx + ncols + 2)
    stdscr.move(uly, ulx)
    stdscr.addstr(text)
    stdscr.move(uly, ulx)

    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines + 2, ulx + ncols + 2)
    stdscr.move(uly, ulx)

    stdscr.move(uly + nlines + 3, ulx)
    stdscr.addstr("[Edit Mode]", curses.color_pair(1))

    stdscr.move(uly, ulx)

    stdscr.refresh()

    while True:

        # check to exit editor
        if screen.exit_editor:
            # second save can be commented out
            # screen.update_save()
            stdscr.move(0, 0)
            stdscr.erase()
            stdscr.refresh()
            return

        op = stdscr.getch()
        c = chr(op)

        try:
            screen.update_screen(op, c, json_path)
            x, y = screen.screen_cursor
            real_x, real_y = screen.cursor

            stdscr.move(uly, ulx)

            camera_row = screen.camera_level
            buffer = screen.buffer
            print_buffer_to_textbox(
                stdscr, camera_row, buffer, nlines, ncols, uly, ulx, real_x, real_y, screen)

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


def view(json_path):
    try:
        # -- Initialize --
        stdscr = curses.initscr()   # initialize curses screen

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(2, curses.COLOR_BLACK, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)

        # colors for coloring
        curses.init_pair(5, curses.COLOR_CYAN, -1)
        curses.init_pair(6, curses.COLOR_GREEN, -1)
        curses.init_pair(7, curses.COLOR_YELLOW, -1)
        curses.init_pair(8, curses.COLOR_RED, -1)
        curses.init_pair(9, curses.COLOR_MAGENTA, -1)

        curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_RED)

        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        curses.noecho()
        curses.cbreak()             # enter break mode where pressing Enter key
        stdscr.keypad(1)

        # -- Perform an action with Screen --

        view_textbox(stdscr, json_path, insert_mode=False)

        while True:
            # stay in this loop till the user presses 'q'
            ch = stdscr.getch()
            # to get char code use str(ch)
            stdscr.addstr(str(ch), curses.color_pair(5))
            stdscr.addstr(" ")

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

    # test()

    json_path = "test.json"
    view(json_path)
