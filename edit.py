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


"""
split_text(text) splits text into a list of strings satisfying the Representation
Invariant

PROPERTY: INverse of Join text
REQUIRES: Split text to initialize string buffer list data structure
"""


def split_text(text):
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


"""
split_at_newline(text, str_list) splits text into constituent strings in
a list separated by \n or \r

If text is empty, returns empty list

REQUIRES: text has less than or equal to 80 characters including all \n and \r
"""


def split_at_newline(text, str_list):
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


"""
join_text(text) joins list of strings into a string of text

PROPERTY: INverse of split_text
"""


def join_text(str_list):
    return "".join(str_list)


l = join_text(l)
print(l)


def shift_lines(str_list):
    pass


def insert(c, x, y, str_list):
    s = str_list[y]
    l_s = len(s)

    s_new = s[0: x] + str(c) + s[x: l_s]
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