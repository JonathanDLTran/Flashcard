# We use Jay Conrod's IMP language

SPACE = " "

SPACES = [" ", "\n", "\t"]

LPAREN = "("
RPAREN = ")"
ASSIGN = ":="
PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
EQ = "="
LT = "<"
GT = ">"
LTE = "<="
GTE = ">="
IF = "if"
ELSE = "else"
WHILE = "while"

# Order matters in keywords
keywords = [
    LPAREN,
    RPAREN,
    ASSIGN,
    LTE,
    GTE,
    EQ,
    LT,
    GT,
    PLUS,
    MINUS,
    TIMES,
    DIV,
    IF,
    ELSE,
    WHILE,
]

keywords_lens = {kw: len(kw) for kw in keywords}

add_space_in_lex = [
    IF,
    ELSE,
    WHILE,
]

no_space_in_lex = [kw for kw in keywords if kw not in add_space_in_lex]

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
    def match_int_helper(string, string_len, idx, num, length):
        # check is there remaining string to process
        if idx >= string_len:
            return (num, length)

        first = string[idx]

        # check var_chars
        if first not in NUMERICAL:
            return (num, length)

        return match_int_helper(string, string_len, idx + 1, num + first, length + 1)
    # check if you have double 0's at beginning, in which case lex fails
    l = len(string)
    if string[idx] == '0' and idx + 1 < l and string[idx + 1] == '0':
        return (None, 0)
    return match_int_helper(string, l, idx, "", 0)


def match_keyword(string, idx, keyword, keywords_lens):
    """
    match_keywords(string, idx, keyword) returns True if kewword matched else False

    keyword_lens is a dictionary mapping keyword to its length
    Requires: the first char of keyword is also shared by string
    """
    l_key = keywords_lens[keyword]
    l_str = len(string)
    if idx + l_key > l_str:
        return False
    return string[idx:(idx + l_key)] == keyword


def match_keywords(string, idx, keywords_lst=keywords, keywords_lens=keywords_lens, space_in_lex=add_space_in_lex):
    """
    match_keywords(string, idx, keywords_lst) returns (keyword, len) for the 
    FIRST matched keyword in keywords_lst

    If no matches returns (None, 0)

    Requires a space after the keyword for a keyword in space_in_lex
    and no space if the keyword is not in space_in_lex. No space is needed if the
    program terminates

    REQUIRES: All \t, \r, \b, \n, \f are replaced with " " space characters already
    in string

    REQUIRES: keywords_lst is ordered in order of importance of lexing

    REQUIRES: idx is an idnex in string

    string is the program string
    idx is the index in the string, must be in stirng
    keyword is a list of strings representing keywords
    space_in_parse is a list of keywords requiring a space after lexing
    """
    for kw in keywords_lst:
        if match_keyword(string, idx, kw, keywords_lens):
            l_key = keywords_lens[kw]
            if kw in space_in_lex:
                l_s = len(string)
                # is the keyword the last characters in the string
                if l_key + idx >= l_s:
                    return (kw, l_key)
                else:
                    if string[l_key + idx] == SPACE:
                        return (kw, l_key)
                    else:
                        # not end with space
                        return (None, 0)
            else:
                return (kw, l_key)
    return (None, 0)


# def match_keywords(program_str, idx, keyword, add_space):
#     if add_space:
#         keyword += SPACE
#     if len(keyword) > len(program_str[idx:]):
#         return False
#     for i in range(len(keyword)):
#         actual_i = i + idx
#         if program_str[actual_i] != keyword[i]:
#             return False
#     return True


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
