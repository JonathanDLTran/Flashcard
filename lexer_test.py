from lexer import *


def test_match_var():
    print("Testing Match Var")

    program = "x = 3"
    m = match_variable(program, 0)
    assert (m == ("x", 1))

    program = "hello_world = 3"
    m = match_variable(program, 0)
    assert (m == ("hello_world", 11))

    program = "hello_world12 = 3"
    m = match_variable(program, 0)
    assert (m == ("hello_world12", 13))

    program = "x0 = 3"
    m = match_variable(program, 0)
    assert (m == ("x0", 2))

    program = "x0 = y0"
    m = match_variable(program, 0)
    assert (m == ("x0", 2))

    program = "x0 = y0"
    m = match_variable(program, 5)
    assert (m == ("y0", 2))

    program = "x0 = y0 + 34"
    m = match_variable(program, 5)
    assert (m == ("y0", 2))

    program = "L"
    m = match_variable(program, 0)
    assert (m == ("L", 1))

    program = "L0"
    m = match_variable(program, 0)
    assert (m == ("L0", 2))

    program = "j k"
    m = match_variable(program, 0)
    assert (m == ("j", 1))

    program = "j k"
    m = match_variable(program, 2)
    assert (m == ("k", 1))

    program = "j k2"
    m = match_variable(program, 2)
    assert (m == ("k2", 2))

    program = "j K2"
    m = match_variable(program, 2)
    assert (m == ("K2", 2))

    program = "S"
    m = match_variable(program, 0)
    assert (m == ("S", 1))

    print("Tested Match Var")


def test_match_int():
    print("Testing Match Int")

    program = "3"
    m = match_int(program, 0)
    assert (m == ("3", 1))

    program = "0"
    m = match_int(program, 0)
    assert (m == ("0", 1))

    program = "100"
    m = match_int(program, 0)
    assert (m == ("100", 3))

    program = "405"
    m = match_int(program, 0)
    assert (m == ("405", 3))

    program = "x = 23"
    m = match_int(program, 4)
    assert (m == ("23", 2))

    program = "x0 = 1219"
    m = match_int(program, 5)
    assert (m == ("1219", 4))

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

    print("Tested Match Var")


def test_match_keywords():
    print("Testing Match Keywords")

    program = "if else"
    m = match_keywords(program, 0)
    assert (m == ("if", 2))

    program = "if else"
    m = match_keywords(program, 3)
    assert (m == ("else", 4))

    program = "if while "
    m = match_keywords(program, 3)
    assert (m == ("while", 5))

    program = "if while"
    m = match_keywords(program, 3)
    assert (m == ("while", 5))

    program = "i"
    m = match_keywords(program, 0)
    assert (m == (None, 0))

    program = "eLSe"
    m = match_keywords(program, 0)
    assert (m == (None, 0))

    program = "+"
    m = match_keywords(program, 0)
    assert (m == ("+", 1))

    program = "-"
    m = match_keywords(program, 0)
    assert (m == ("-", 1))

    program = "*"
    m = match_keywords(program, 0)
    assert (m == ("*", 1))

    program = "/"
    m = match_keywords(program, 0)
    assert (m == ("/", 1))

    program = "("
    m = match_keywords(program, 0)
    assert (m == ("(", 1))

    program = ")"
    m = match_keywords(program, 0)
    assert (m == (")", 1))

    program = ">"
    m = match_keywords(program, 0)
    assert (m == (">", 1))

    program = "<"
    m = match_keywords(program, 0)
    assert (m == ("<", 1))

    program = ">="
    m = match_keywords(program, 0)
    assert (m == (">=", 2))

    program = "<="
    m = match_keywords(program, 0)
    assert (m == ("<=", 2))

    program = "x:=3"
    m = match_keywords(program, 1)
    assert (m == (":=", 2))

    print("Tested Match Keywords")


def test_get_var():
    print("Testing Get Var")
    program = "if else"
    assert (get_var(program, 0) == "if")
    assert (get_var(program, 3) == "else")
    print("Tested Get Var")


if __name__ == "__main__":
    test_get_var()
    test_match_var()
    test_match_int()
    test_match_keywords()