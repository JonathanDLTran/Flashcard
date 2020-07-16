from lexer import *


def test_match_var():
    print("Testing Match Var")

    program = "??!x = 3"
    m = match_variable(program, 0)
    assert (m == (None, 0))

    program = "  x = 3"
    m = match_variable(program, 0)
    assert (m == (None, 0))

    program = "3x = 3"
    m = match_variable(program, 0)
    assert (m == (None, 0))

    program = "312xx = 3"
    m = match_variable(program, 0)
    assert (m == (None, 0))

    program = "x = 3"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "x"), 1))

    program = "hello_world = 3"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "hello_world"), 11))

    program = "hello_world12 = 3"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "hello_world12"), 13))

    program = "x0 = 3"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "x0"), 2))

    program = "x0 = y0"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "x0"), 2))

    program = "x0 = y0"
    m = match_variable(program, 5)
    assert (m == ((VARIABLE, "y0"), 2))

    program = "x0 = y0 + 34"
    m = match_variable(program, 5)
    assert (m == ((VARIABLE, "y0"), 2))

    program = "L"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "L"), 1))

    program = "L0"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "L0"), 2))

    program = "j k"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "j"), 1))

    program = "j k"
    m = match_variable(program, 2)
    assert (m == ((VARIABLE, "k"), 1))

    program = "j k2"
    m = match_variable(program, 2)
    assert (m == ((VARIABLE, "k2"), 2))

    program = "j K2"
    m = match_variable(program, 2)
    assert (m == ((VARIABLE, "K2"), 2))

    program = "S"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "S"), 1))

    program = "_"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "_"), 1))

    program = "_x"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "_x"), 2))

    program = "__"
    m = match_variable(program, 0)
    assert (m == ((VARIABLE, "__"), 2))

    print("Tested Match Var")


def test_match_int():
    print("Testing Match Int")

    program = "3"
    m = match_int(program, 0)
    assert (m == ((INTEGER, 3), 1))

    program = "0"
    m = match_int(program, 0)
    assert (m == ((INTEGER, 0), 1))

    program = "100"
    m = match_int(program, 0)
    assert (m == ((INTEGER, 100), 3))

    program = "405"
    m = match_int(program, 0)
    assert (m == ((INTEGER, 405), 3))

    program = "x = 23"
    m = match_int(program, 4)
    assert (m == ((INTEGER, 23), 2))

    program = "x0 = 1219"
    m = match_int(program, 5)
    assert (m == ((INTEGER, 1219), 4))

    # test no leading 0's
    program = "00"
    m = match_int(program, 0)
    assert (m == (None, 0))

    program = "007"
    m = match_int(program, 0)
    assert (m == (None, 0))

    program = "ssh1 007"
    m = match_int(program, 5)
    assert (m == (None, 0))

    program = "00001007"
    m = match_int(program, 0)
    assert (m == (None, 0))

    program = "a"
    m = match_int(program, 0)
    assert (m == (None, 0))

    program = "Lasda"
    m = match_int(program, 0)
    assert (m == (None, 0))

    program = "3.01"
    m = match_int(program, 0)
    assert (m == (FLOAT, 3.01), 4)

    program = "0.01"
    m = match_int(program, 0)
    assert (m == (FLOAT, 3.01), 4)

    program = "12100.0"
    m = match_int(program, 0)
    assert (m == (FLOAT, 12100.0), 7)

    print("Tested Match Var")


def test_match_keywords():
    print("Testing Match Keywords")

    program = "if else"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "if"), 2))  # add space

    program = "if else"
    m = match_keywords(program, 3)
    assert (m == ((KEYWORD, "else"), 4))

    program = "if while "
    m = match_keywords(program, 3)
    assert (m == ((KEYWORD, "while"), 5))

    program = "if while"
    m = match_keywords(program, 3)
    assert (m == ((KEYWORD, "while"), 5))

    program = "i"
    m = match_keywords(program, 0)
    assert (m == (None, 0))

    program = "eLSe"
    m = match_keywords(program, 0)
    assert (m == (None, 0))

    program = "+"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "+"), 1))

    program = "-"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "-"), 1))

    program = "*"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "*"), 1))

    program = "/"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "/"), 1))

    program = "("
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "("), 1))

    program = ")"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, ")"), 1))

    program = ">"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, ">"), 1))

    program = "<"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "<"), 1))

    program = ">="
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, ">="), 2))

    program = "<="
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "<="), 2))

    program = "x:=3"
    m = match_keywords(program, 1)
    assert (m == ((KEYWORD, ":="), 2))

    program = "True False"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "True"), 4))

    program = "True False"
    m = match_keywords(program, 5)
    assert (m == ((KEYWORD, "False"), 5))

    program = "fun -> endfun"
    m = match_keywords(program, 0)
    assert (m == ((KEYWORD, "fun"), 3))

    program = "fun -> endfun    "
    m = match_keywords(program, 4)
    assert (m == ((KEYWORD, "->"), 2))

    program = "fun -> endfun "
    m = match_keywords(program, 7)
    assert (m == ((KEYWORD, "endfun"), 6))

    print("Tested Match Keywords")


def test_str():
    print("Testing Match String")

    program = '"hello world!"'
    m = match_string(program, 0)
    assert (m == ((STRING, "hello world!"), len(program)))

    program = '""'
    m = match_string(program, 0)
    assert (m == ((STRING, ""), len(program)))

    program = '"h"'
    m = match_string(program, 0)
    assert (m == ((STRING, "h"), len(program)))

    print("Tested Match String")


def test_lex():
    print("Testing Lex")

    program = "if else"
    m = lex(program)
    assert (m == [(KEYWORD, "if"), (KEYWORD, "else")])

    program = 'if else "hello"'
    m = lex(program)
    assert (m == [(KEYWORD, "if"), (KEYWORD, "else"), (STRING, "hello")])

    program = 'if else  "hello"  '
    m = lex(program)
    assert (m == [(KEYWORD, "if"), (KEYWORD, "else"), (STRING, "hello")])

    program = '"lol" if else  "hello"  '
    m = lex(program)
    assert (m == [(STRING, "lol"), (KEYWORD, "if"),
                  (KEYWORD, "else"), (STRING, "hello")])

    program = ' "lol"if else  "hello"  '
    m = lex(program)
    assert (m == [(STRING, "lol"), (KEYWORD, "if"),
                  (KEYWORD, "else"), (STRING, "hello")])

    program = ' if "lol"else  "hello"  '  # if needs a space after!
    m = lex(program)
    assert (m == [(KEYWORD, "if"), (STRING, "lol"),
                  (KEYWORD, "else"), (STRING, "hello")])

    program = "x:=3"
    m = lex(program)
    assert (m == [(VARIABLE, "x"), (KEYWORD, ":="), (INTEGER, 3)])

    program = "x := 3"
    m = lex(program)
    assert (m == [(VARIABLE, "x"), (KEYWORD, ":="), (INTEGER, 3)])

    program = "x2:=343"
    m = lex(program)
    assert (m == [(VARIABLE, "x2"), (KEYWORD, ":="), (INTEGER, 343)])

    program = "     x2:= 343  23            "
    m = lex(program)
    assert (m == [(VARIABLE, "x2"), (KEYWORD, ":="),
                  (INTEGER, 343), (INTEGER, 23)])

    program = "  True   x2:= 343  23  False    "
    m = lex(program)
    assert (m == [(KEYWORD, "True"), (VARIABLE, "x2"), (KEYWORD, ":="),
                  (INTEGER, 343), (INTEGER, 23), (KEYWORD, "False")])

    program = "  fun x y -> x*y endfun   "
    m = lex(program)
    assert (m == [(KEYWORD, "fun"), (VARIABLE, "x"), (VARIABLE, "y"), (KEYWORD, "->"),
                  (VARIABLE, "x"), (KEYWORD, "*"), (VARIABLE, "y"), (KEYWORD, "endfun")])

    program = "  fun x y -> x*y endfun   "
    m = lex(program)
    assert (m == [(KEYWORD, "fun"), (VARIABLE, "x"), (VARIABLE, "y"), (KEYWORD, "->"),
                  (VARIABLE, "x"), (KEYWORD, "*"), (VARIABLE, "y"), (KEYWORD, "endfun")])

    program = "  fun x y -> while x > 0 x*y endfun   "
    m = lex(program)
    assert (m == [(KEYWORD, "fun"), (VARIABLE, "x"), (VARIABLE, "y"), (KEYWORD, "->"), (KEYWORD, "while"),
                  (VARIABLE, "x"), (KEYWORD, ">"), (INTEGER, 0), (VARIABLE, "x"), (KEYWORD, "*"), (VARIABLE, "y"), (KEYWORD, "endfun")])

    program = "  True  ?? x2:= 343  23  False    "
    try:
        m = lex(program)
        assert False
    except TOKENIZATION_ERROR:
        assert True

    print("Tested Lex")


if __name__ == "__main__":
    test_lex()
    test_match_var()
    test_match_int()
    test_str()
    test_match_keywords()
