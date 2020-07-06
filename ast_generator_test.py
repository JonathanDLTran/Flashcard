from lexer import *
from ast_generator import *


def test_match_expr():
    print("Testing Match Expr")

    program = "3 + 4"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)
    # assert (ast == [(KEYWORD, "if"), (KEYWORD, "else")])

    program = "3 * 4 + 5"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "3 + 4 * 5"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "3 + 4 * 5 / 6"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "3 * 4 + 5 / 6"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "3 * 4 - 6"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-3"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-3"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-10 + -20"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-10 + -20 * 30"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "5 * -10 + -20 * 30"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "3 * 5 * -10/4 + 7--20 * 30"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "1 -- 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-1 -- 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-1 + -1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(1 + 1)"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(1 + 1) + 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "2 * (1 + 1) + 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(1/ 2) * (1 + 1) + 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(1/ (2 + 3)) * (1 + 1) + 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "()"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "((1 + ((1 + (1 + ((1 + 1)))))))"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(((1)))"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "(((-1)))"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "4 + -3 * (-1 + -2) - 5"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "4 * -3 * 2 + 1"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    program = "-(1)"
    lexbuf = lex(program)
    ast = match_expr(None, lexbuf)
    print(ast)

    print("Tested Match Expr")


if __name__ == "__main__":
    test_match_expr()
