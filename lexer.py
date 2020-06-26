# We use Jay Conrod's IMP language

SPACE = " "

SPACES = [" ", "\n", "\t"]

LPAREN = "("
RPAREN = ")"
ASSIGN = ":="
EQ = "="
LT = "<"
GT = ">"
LTE = "<="
GTE = ">="
IF = "if"
ELSE = "else"
WHILE = "while"

keywords = [
    ASSIGN,
    EQ,
    LT,
    GT,
    LTE,
    GTE,
    IF,
    ELSE,
    WHILE,
]

add_space_in_parse = [
    IF,
    ELSE,
    WHILE,
]

no_space_in_parse = [kw for kw in keywords if kw not in add_space_in_parse]

ALPHABETICAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMERICAL = "0123456789"
UNDERSCORE = "_"

variable_chars = [
    ALPHABETICAL,
    NUMERICAL,
    UNDERSCORE,
]

VARIABLE_NOT_START_NUMERIC = True


def match_variable(string, idx, var_chars=variable_chars):
    """
    match_variable(str, idx, var_chars, var_rules) checks if the str beginnign
    at idx is a variable and returns the variable name and the lenght if the variable
    based on the character rules allowed for a variable name in var_chars

    Returns (var_name, len) if possible, else (None, 0)
    Requires: idx in str could be the start of a variable, and so thus, the first
    cannot be a numeral
    """
    def match_variable_helper(string, idx, var_chars, name, length):
        # check is there remaining string to process
        if idx >= len(string):
            return (name, length)

        first = string[idx]

        # check var_chars
        correct_char = False
        for var_str in var_chars:
            if first in var_str:
                correct_char = True
                break
        if not correct_char:
            return (name, length)

        return match_variable_helper(string, idx + 1, var_chars, name + first, length + 1)

    n, l = match_variable_helper(string, idx, var_chars, "", 0)
    if l == 0:
        return None, 0
    return (n, l)


def match_int(string, idx):
    """
    match_int(string, idx) is an integer stirng and the length of the string if
    wtring matches 

    Requires: string begins at an integer location

    Only matches positive ints!
    Requires: idx does not start at alocation not corresponding to an int
    """
    def match_int_helper(string, idx, num, length):
        # check is there remaining string to process
        if idx >= len(string):
            return (num, length)

        first = string[idx]

        # check var_chars
        if first not in NUMERICAL:
            return (num, length)

        return match_int_helper(string, idx + 1, num + first, length + 1)
    return match_int_helper(string, idx, "", 0)


def match_keywords(program_str, idx, keyword, add_space):
    if add_space:
        keyword += SPACE
    if len(keyword) > len(program_str[idx:]):
        return False
    for i in range(len(keyword)):
        actual_i = i + idx
        if program_str[actual_i] != keyword[i]:
            return False
    return True


def match_first_keyword(program_str, idx, keyword_list, add_space):
    for kw in keyword_list:
        if match_keywords(program_str, idx, kw, add_space):
            return kw
    return None


def match_char(char, keywords_list):
    kws = []
    for kw in keywords_list:
        if kw[0] == char:
            kws.append(kw)
    return kws


def get_var(program_str, idx):
    l = len(program_str)
    var_name = ""
    while (idx < l):
        c = program_str[idx]
        if c in SPACES:
            return var_name
        var_name += c
        idx += 1
    return var_name


def lex(program_str):
    """
    program_str is striped already, beigns and ends on char
    Lex is recursive
    We have the invariant as below:
    0. If we match character with a kwyword, check if it is a keyword and
    lex it, no space is needed after it (e.g. a left paren, right paren, equals
    <=, etc)
    1. (With Spaces) If we match characters with a keyword, check to see if it is a keyword
        a. Keyword if match and also space at end
        b. Keyword if match and string ended already (no space at end)
    2. If we have a character not matched with a keyword, it is part of a var
        a. Variable if it only has alphabeticals, and _ numerics and end,
            i .terminating the variable when a space is reached OR
            ii. a non alphabetical isreached
            III. When a () parentheses is reached
    3. Numbers are numerics and are pulled out, only iotegers
    4. Spaces are eliminated
    5. If not all consumed, terminate

    """

    tokens = []
    is_var = False
    var_name = ""
    l = len(program_str)
    i = 0
    while (i != l):
        char = program_str[i]
        if not is_var:
            match_keywords_list = match_char(char, keywords)
            kw = match_first_keyword(
                program_str, i, match_keywords_list, False)
            # need to change true condition
            if kw != None:
                tokens.append(kw)
                l = len(kw)
                i += l

            else:
                is_var = True
                var_name += char
                i += 1
        else:
            if char == SPACE:
                is_var = False
                tokens.append(var_name)
                var_name = ""
                i += 1
            else:
                var_name += char
                i += 1
    return tokens


if __name__ == "__main__":
    program = "if else"
    print(lex(program))
