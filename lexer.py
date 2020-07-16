# We use Jay Conrod's IMP language

# ------- CONSTANTS ---------
SPACE = " "

SPACES = [" ", "\n", "\t"]

# Spaces to preprocess out of program string
ILLEGAL_SPACES = ["\b", "\n", "\t", "\f", "\r"]

COMMA = ","
SEMI = ";"
EXP = "**"
LPAREN = "("
RPAREN = ")"
PLUS = "+"
FUN_ARROW = "->"
MINUS = "-"
TIMES = "*"
DIV = "/"
EQ = "="
LT = "<"
GT = ">"
ASSIGN = ":="
LTE = "<="
GTE = ">="
FUN = "fun"
END_FUN = "endfun"
TRUE = "True"
FALSE = "False"
IF = "if"
THEN = "then"
ELIF = "elif"
ELSE = "else"
ENDIF = "endif"
ENDELIF = "endelif"
ENDELSE = "endelse"
WHILE = "while"
DO_WHILE = "dowhile"
END_WHILE = "endwhile"
FOR = "for"
FROM = "from"
TO = "to"
BY = "by"
DOFOR = "dofor"
ENDFOR = "endfor"
RETURN = "return"
IGNORE = "~"
DOUBLE_QUOTE = '"'
OPEN_TUP = "(|"
CLOSE_TUP = "|)"


# Order matters in keywords
keywords = sorted(
    [
        IGNORE,
        COMMA,
        SEMI,
        EXP,
        LPAREN,
        RPAREN,
        FUN_ARROW,
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
        TRUE,
        FALSE,
        FUN,
        IF,
        ELSE,
        ELIF,
        THEN,
        ENDIF,
        ENDELIF,
        ENDELSE,
        WHILE,
        DO_WHILE,
        END_WHILE,
        END_FUN,
        FOR,
        FROM,
        TO,
        BY,
        DOFOR,
        ENDFOR,
        RETURN,
        OPEN_TUP,
        CLOSE_TUP,

    ],
    reverse=True)

UNOPS = [
    MINUS,
]

BOPS = [
    EXP,
    LTE,
    GTE,
    EQ,
    LT,
    GT,
    PLUS,
    MINUS,
    TIMES,
    DIV,
]

OPERATIONS = UNOPS + BOPS

keywords_lens = {kw: len(kw) for kw in keywords}

add_space_in_lex = [
    FUN,
    END_FUN,
    TRUE,
    FALSE,
    IF,
    THEN,
    ELSE,
    ELIF,
    ENDIF,
    ENDELIF,
    ENDELSE,
    WHILE,
    DO_WHILE,
    END_WHILE,
    FOR,
    FROM,
    TO,
    BY,
    DOFOR,
    ENDFOR,
    RETURN,
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


# ------ TOKEN TYPES -------

VARIABLE = "variable"
INTEGER = "integer"
STRING = "string"
KEYWORD = "keyword"


# ------ EXCEPTIONS --------


class TOKENIZATION_ERROR(Exception):
    """
    Raised when tokenization fails
    """
    pass


# ------- MATCH TOKENS FUNCTIONS --------


def match_variable(string, idx, var_chars=variable_chars):
    """
    match_variable(str, idx, var_chars, var_rules) checks if the str beginnign
    at idx is a variable and returns the variable name and the lenght if the variable
    based on the character rules allowed for a variable name in var_chars

    Returns (var_name, len) if possible, else (None, 0)
    Returns (None, 0) if string does not being with a variable allowed char, like udnerscore or
    alphabetical
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

    # check if the first character could be variable:
    if (string[idx] not in UNDERSCORE) and (string[idx] not in ALPHABETICAL):
        return (None, 0)

    v, l = match_variable_helper(string, idx, var_chars, "", 0)

    # no match
    if l == 0:
        return (None, 0)

    # variable cannot start with numeric
    if VARIABLE_NOT_START_NUMERIC and v[0] in NUMERICAL:
        return (None, 0)

    return ((VARIABLE, v), l)


def match_int(string, idx):
    """
    match_int(string, idx) is an integer stirng and the length of the string if
    wtring matches

    Requires: string begins at an integer location

    Returns (NOne, 0) if string does not begin with an int
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

    # check it begins with an int
    if string[idx] not in NUMERICAL:
        return (None, 0)

    # check if you have double 0's at beginning, in which case lex fails
    l = len(string)
    if string[idx] == '0' and idx + 1 < l and string[idx + 1] == '0':
        return (None, 0)

    i, l = match_int_helper(string, l, idx, "", 0)
    return ((INTEGER, int(i)), l)


def match_string(string, idx):
    """
    match_string(string, idx) matches a string and the length of the string
    and returns (String, str), length

    REQUIRES: stirng begins at a string location, e.g. with an open double quote
    so tht idx is the location of a double quote, and idx + 1is the first locaiton
    after that double quote
    """
    l = len(string)
    collect_string = ""
    for i in range(idx + 1, l):
        c = string[i]
        if c != DOUBLE_QUOTE:
            collect_string += c
        else:
            # add 2 for start and end quotes
            return ((STRING, str(collect_string)), len(collect_string) + 2)


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

    WARNING: DOES NOT INCLUDE SPACE IN THE KEYWORD LENGTH THAT IS RETURNED;
    IGNORES SPACE AFTER KEYWORD THAT NEEDS SPACE

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
                    return ((KEYWORD, kw), l_key)
                else:
                    if string[l_key + idx] == SPACE:
                        return ((KEYWORD, kw), l_key)
                    else:
                        # not end with space
                        return (None, 0)
            else:
                return ((KEYWORD, kw), l_key)
    return (None, 0)


# ----- PREPROCESSING PROGRAM -------


def clean_spaces(program_str):
    """
    Removes: \n, \r, \t, \f, \b and replaces with spaces
    Strips at front and end
    Returns cleaned program string
    """
    program_str = program_str.strip()
    for c in ILLEGAL_SPACES:
        program_str = program_str.replace(c, SPACE)
    return program_str


def preprocess(program_str):
    """
    preprocess(program_str) preprocesses the program string
    Removes: \n, \r, \t, \f, \b and replaces with spaces
    Strips at front and end

    Return preprocessed program_str
    """
    return clean_spaces(program_str)

# ------ LEXER ------


def lex(program_str):
    """
    LEXER/TOKENIZER
    Progam_str is a string of the program source code

    Returns list of Tokens

    Starts by Preprocesses program string

    Lex is recursive
    We have the invariant as below:
    END if program_str is empty!
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
    4. Strings begin double quote and end with double quote
    5. Spaces are eliminated
    6. If not all consumed, terminate by raising 
    """
    def lex_helper(program_str, acc):
        if program_str == "":
            return acc

        token, length = match_keywords(program_str, 0)
        if token != None:
            return lex_helper(program_str[length:], acc + [token])

        token, length = match_variable(program_str, 0)
        if token != None:
            return lex_helper(program_str[length:], acc + [token])

        token, length = match_int(program_str, 0)
        if token != None:
            return lex_helper(program_str[length:], acc + [token])

        if program_str[0] == DOUBLE_QUOTE:
            token, length = match_string(program_str, 0)
            return lex_helper(program_str[length:], acc + [token])

        if program_str[0] == SPACE:
            return lex_helper(program_str[1:], acc)

        raise TOKENIZATION_ERROR("Could not consume characters")

    return lex_helper(preprocess(program_str), [])


if __name__ == "__main__":
    pass
