"""
Grammar:
Variable ::= 
    | [a-zA-z etc.]
Boolean ::= 
    | True
    | False
Value ::= 
    | Boolean
    | Int i
BOP ::=
    | + 
    | - 
    | / 
    | * 
    | and
    | or

UNOP ::=
 | -
 | not
Expression ::= 
| Value
| Variable
| (e1)
| [e1] bop [e2]
| while [e1] do [e2] endwhile
| if [e1] then [e2] else [e3]

Sentence ::=
    | Variable := e
    # | Variable = fun [optional] [v1] [v2] ... -> [e] endfun e.g. fun -> return 4 endfun


"""

import lexer


class AST:
    """
    AST is an abstract syntax tree
    """

    def __init__(self):
        pass


def match_bop(lex_buff, bops_list):
    pass


def parse(lex_buff):
    def parse_helper(lex_buff, ast, stack):
        if lex_buff == []:
            return
    return parse_helper(lex_buff, AST(), [])
