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


# ------- GRAMMAR PRODUCTION RULES ------------fds

VALUE = 'value'
INTEGER = 'integer'
BOOLEAN = 'boolean'
EXPRESSION = 'expression'
# BOP = "bop"

VALUE_RULES = [
    [INTEGER],
    [BOOLEAN],
]

BOPS = [
    lexer.PLUS,
    lexer.MINUS,
    lexer.TIMES,
    lexer.DIV,
]

EXPRESSION_RULES = [
    [VALUE],
    [EXPRESSION, BOP, EXPRESSION],
    []

]

# ------ EXCEPTIONS ---------


class MissingParens(Exception):
    def __init__(self, str):
        pass


class ParseError(Exception):
    def __init__(self, str):
        pass

# ------ AST CLASSES --------


class AST:
    """
    AST is an abstract syntax tree
    """

    def __init__(self):
        self.sentences = []

    def is_empty(self):
        return self.sentences == []


class Expr(object):
    """
    Expr respresents an expression

    ABSTRACT CLASS for all instantiated expression classes
    """

    def __init__(self):
        pass

    def __repr__(self):
        return "This is a abstract expression"


class IntValue(Expr):
    """
    IntValue represents an Int Value 
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return "IntValue: " + str(self.value)


class Bop(Expr):
    """
    Bop represents e1 bop e2
    """

    def __init__(self, bop, left=None, right=None):
        super().__init__()
        self.bop = bop
        self.left = left
        self.right = right

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def __repr__(self):
        return "BOP: " + str(self.left) + str(self.bop) + str(self.right)


class Unop(Expr):
    """
    Unop represents unop e
    """

    def __init__(self, unop, expr=None):
        uper().__init__()
        self.unop = unop
        self.expr = expr

    def set_expr(self, expr):
        self.expr = expr

    def __repr__(self):
        return "UNOP: " + str(self.unop) + str(self.expr)


# ------ MATCH FUNCTIONS --------

def match_value(lex_buff, idx):
    lex_typ, val = lex_buff[idx]
    if lex_typ != lexer.INTEGER:
        return None
    return Value(val, lex_typ)


def get_between_brackets(lex_buff, idx):
    # assume start after idx
    stack = []
    stack.append(lexer.LPAREN)
    expr_terms = []
    i = idx
    while (i < len(lex_buff) and stack != []):
        _, val = lex_buff[i]
        if val == lexer.LPAREN:
            stack.append(val)
        elif val == lexer.RPAREN:
            if stack != [] and stack[-1] == lexer.LPAREN:
                stack.pop()
        expr_terms.append(val)
        i += 1

    if i >= len(lex_buff):
        raise MissingParens("Missing or Misplaced Parentheses")
    if stack != []:
        raise MissingParens("Missing or Misplaced Parentheses")
    l = len(expr_terms)
    expr_terms.pop()  # removd last parentheses
    return (expr_terms, l)


def match_open_paren(ast, lex_buff, idx):
    lex_typ, val = lex_buff[idx]
    if val != lexer.LPAREN:
        return None
    middle_terms, length = get_between_brackets(lex_buff, idx + 1)
    new_lex_buff = lex_buff[idx + 1 + length:]
    new_ast = match_expr(ast, middle_terms)
    return match_expr(new_ast, new_lex_buff)


def match_bop(ast, lex_buff):
    lex_typ, val = lex_buff[0]
    if val == lexer.PLUS:
        if ast.is_empty():
            raise issue:
        bop_node = BOP(lexer.PLUS, ast, None)
        return bop_node


def match_expr(ast, lexbuf):
    """
    match_expr(ast, lexbuf) creates an ast from lexbuf, otherwise raises 
    appropriate execption
    """
    if lexbuf == []:
        return ast

    typ, val = lexbuf[0]
    tail = lexbuf[1:]

    if typ == lexer.INTEGER:
        return match_integer(tail, val)
    elif ast == None and typ in lexer.BOPS:
        raise Bop_Missing_Arg("Missing arg %s" % (val))
    elif ast != None and typ in lexer.BOPS:
        return match_bop(ast, tail, val)
    elif ast == None and typ in lexer.UNOPS:
        return match_unop(tail, val)
    elif ast != None and typ in lexer.UNOPS:
        raise Unop_Additional_Arg(
            "Additional arg to a unary operation %s" % (val))
    elif typ == lexer.LPAREN:
        return match_lparent(ast, tail, val)
    elif typ == lexer.RPAREN:
        raise Unmatched_Paren_Error("Unmatched right parentehesis %s" % (val))

    raise MatchError


def match(lexbuf):
    """
    match(lexbuf) creates an ast from from lexbuf, otherwises
    raises an appropriate exeception
    """
    ast = None
    return match_expr(ast, lexbuf)


def parse(lex_buff):
    def parse_helper(lex_buff, ast, stack):
        if lex_buff == []:
            return
    return parse_helper(lex_buff, AST(), [])