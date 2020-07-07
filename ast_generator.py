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

# VALUE = 'value'
# INTEGER = 'integer'
# BOOLEAN = 'boolean'
# EXPRESSION = 'expression'
# # BOP = "bop"

# VALUE_RULES = [
#     [INTEGER],
#     [BOOLEAN],
# ]

# BOPS = [
#     lexer.PLUS,
#     lexer.MINUS,
#     lexer.TIMES,
#     lexer.DIV,
# ]

# EXPRESSION_RULES = [
#     [VALUE],
#     [EXPRESSION, BOP, EXPRESSION],
#     []

# ]

from copy import deepcopy

# ------ EXCEPTIONS ---------


class MissingParens(Exception):
    def __init__(self, str):
        pass


class ParseError(Exception):
    def __init__(self, str):
        pass


class BopMissingArg(Exception):
    def __init__(self, str):
        pass


class UnopAdditionalArg(Exception):
    def __init__(self, str):
        pass


class UnmatchedParenError(Exception):
    def __init__(self, str):
        pass


class EndWithOperatorError(Exception):
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
        return "(IntValue: " + str(self.value) + ")"


class VarValue(Expr):
    """
    IntValue represents an Variable Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return "(VarValue: " + str(self.value) + ")"


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
        return "(BOP: " + str(self.left) + str(self.bop) + str(self.right) + ")"


class Unop(Expr):
    """
    Unop represents unop e
    """

    def __init__(self, unop, expr=None):
        super().__init__()
        self.unop = unop
        self.expr = expr

    def set_expr(self, expr):
        self.expr = expr

    def __repr__(self):
        return "(UNOP: " + str(self.unop) + str(self.expr) + ")"


# ------ MATCH FUNCTIONS --------

def match_integer(lexbuf, val):
    return match_expr(IntValue(val), lexbuf)


def get_between_brackets(lex_buff, idx):
    # assume start after idx
    stack = []
    stack.append(lexer.LPAREN)
    expr_terms = []
    i = idx

    while (i < len(lex_buff) and stack != []):

        typ, val = lex_buff[i]
        if val == lexer.LPAREN:
            stack.append(val)
        elif val == lexer.RPAREN:
            if stack != [] and stack[-1] == lexer.LPAREN:
                stack.pop()
        expr_terms.append((typ, val))
        i += 1

    if i > len(lex_buff):
        raise MissingParens("Missing or Misplaced Parentheses")
    if stack != []:
        raise MissingParens("Missing or Misplaced Parentheses")
    l = len(expr_terms)
    expr_terms.pop()  # removd last parentheses
    return (expr_terms, l)


def match_open_paren(ast, lex_buff):

    lex_typ, val = lex_buff[0]
    if val != lexer.LPAREN:
        return None

    middle_terms, length = get_between_brackets(lex_buff[1:], 0)
    new_lex_buff = lex_buff[1 + length:]
    new_ast = match_expr(None, middle_terms)

    if ast != None:
        ast.set_right(new_ast)

    else:
        ast = new_ast

    return match_expr(ast, new_lex_buff)


def match_bop(ast, lexbuf, bop):
    bop_node = Bop(bop)
    bop_node.set_left(ast)
    # need to wrap in try.except if theis is undefined
    head = lexbuf[0]
    la_typ, la_val = head
    if (bop == lexer.TIMES or bop == lexer.DIV) and la_typ in lexer.INTEGER:
        right_node = match_expr(None, [head])
        bop_node.set_right(right_node)
        tail = lexbuf[1:]
        return match_expr(bop_node, tail)
    elif (bop == lexer.TIMES or bop == lexer.DIV) and la_val == lexer.LPAREN:
        right_node = match_open_paren(bop_node, lexbuf)
        return right_node
    else:
        right_node = match_expr(None, lexbuf)
        bop_node.set_right(right_node)

    return bop_node


def match_unop(lexbuf, unop):
    unop_node = Unop(unop)
    head = lexbuf[0]
    tail = lexbuf[1:]
    la_typ, _ = head
    if la_typ in lexer.INTEGER:
        bottom_node = match_expr(None, [head])
        unop_node.set_expr(bottom_node)
        return match_expr(unop_node, tail)
    raise UnopAdditionalArg(
        "Additional arg to a unary operation %s" % (unop))


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
    elif ast == None and val in lexer.UNOPS:
        return match_unop(tail, val)
    elif ast == None and val in lexer.BOPS:
        raise BopMissingArg("Missing arg %s" % (val))
    elif ast != None and val in lexer.BOPS:
        return match_bop(ast, tail, val)
    elif ast != None and val in lexer.UNOPS:
        raise UnopAdditionalArg(
            "Additional arg to a unary operation %s" % (val))
    elif val == lexer.LPAREN:
        return match_open_paren(ast, lexbuf)
        # return match_lparent(ast, tail, val)
    elif val == lexer.RPAREN:
        raise UnmatchedParenError("Unmatched right parenthesis %s" % (val))

    raise ParseError("Error in Parsing Tokens")


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


PRECENDENCE_MAP = {
    lexer.PLUS: 1,
    lexer.MINUS: 1,
    lexer.TIMES: 2,
    lexer.DIV: 2,
    lexer.EXP: 3,
}


def get_precedence(symbol, precendence_map=PRECENDENCE_MAP):
    return precendence_map[symbol]


def reduce_stack(precedence, stack):
    """
    reduce_stack(stack) reduces the stack from the top of the stack
    to the end into a unified AST at precedence level precedence

    REQUIRES: [precendence] cannot be 0
    REQUIRES: STACK is NOT EMPTY
    REQUIRES: STACK MUST BE ABLE TO TURNED INTO A VALID AST, E>G> A STACK WITH ONE ELEMENT
    MUST BE A VALUE OR VARIABLE!
    If the stack has one element, returns that element
    """
    assert stack != []

    l = len(stack)
    if l == 1:
        return stack[0]

    if precedence <= 3:
        end_stack = stack[:3]
        bop = end_stack[1][1]
        start = end_stack[0]
        end = end_stack[2]
        new_stack = deepcopy(stack[3:])
        new_stack.insert(0, Bop(bop, start, end))
        return reduce_stack(precedence, new_stack)

    elif precedence == 4:
        unop = stack[0]
        val = stack[1]
        new_stack = deepcopy(stack[2:])
        new_stack.insert(0, Unop(unop, val))
        return reduce_stack(precedence, new_stack)
    # elif precedence == 2:
    #     end_stack = stack[:3]
    #     bop = end_stack[1][1]
    #     start = end_stack[0]
    #     end = end_stack[2]
    #     new_stack = deepcopy(stack[3:])
    #     new_stack.insert(0, Bop(bop, start, end))
    #     return reduce_stack(precedence, new_stack)


def parse_expr(prev_precedence, count, precedence, stack, lexbuf):

    # nothing more to parse
    if lexbuf == []:
        return (count, reduce_stack(precedence, stack))

    typ_curr, val_curr = lexbuf[0]
    if len(lexbuf) <= 1:
        new_stack = deepcopy(stack)
        if typ_curr == lexer.INTEGER:
            new_stack.append(IntValue(val_curr))
        elif typ_curr == lexer.VARIABLE:
            new_stack.append(VarValue(val_curr))
        else:
            raise EndWithOperatorError(val_curr)
        return (count + 1, reduce_stack(precedence, new_stack))

    type_la, val_la = lexbuf[1]
    if typ_curr == lexer.INTEGER:
        if type_la == lexer.INTEGER or type_la == lexer.VARIABLE:
            raise ParseError

        new_precedence = get_precedence(val_la, PRECENDENCE_MAP)

        if new_precedence > precedence:
            new_stack = []
            new_stack.append(IntValue(val_curr))
            new_idx, res_ast = parse_expr(precedence,
                                          0, new_precedence, new_stack, lexbuf[1:])
            stack.append(res_ast)
            return parse_expr(prev_precedence, count + new_idx + 1, precedence, stack, lexbuf[1 + new_idx:])

        elif new_precedence == precedence:
            stack.append(IntValue(val_curr))
            # reduced_stack = reduce_stack(precedence, stack)
            return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[1:])

        else:

            stack.append(IntValue(val_curr))
            res_ast = reduce_stack(precedence, stack)
            next_precedence = get_precedence(
                lexbuf[1][1], PRECENDENCE_MAP) if len(lexbuf) >= 2 else -1
            if prev_precedence < next_precedence:
                next_stack = []
                next_stack.append(res_ast)

                return parse_expr(precedence, count + 1, next_precedence, next_stack, lexbuf[1:])
            return count + 1, res_ast
            # return parse_expr(0, new_precedence, [], lexbuf[1:])

    elif val_curr in lexer.OPERATIONS:

        if stack == []:
            # unop case (Negation)
            new_stack = []
            new_stack.append(lexbuf[0])
            unop_precedence = 4
            shift, res_ast = parse_expr(
                precedence, 0, unop_precedence, new_stack, lexbuf[1:])
            stack.append(res_ast)

            return parse_expr(prev_precedence, count + shift + 1, precedence, stack, lexbuf[1 + shift:])
        elif val_la in lexer.UNOPS:

            # unop case (Negation)
            new_stack = []
            stack.append(lexbuf[0])
            new_stack.append(lexbuf[1])
            unop_precedence = 4
            shift, res_ast = parse_expr(
                precedence, 1, unop_precedence, new_stack, lexbuf[2:])
            stack.append(res_ast)

            return parse_expr(prev_precedence, count + shift + 1, precedence, stack, lexbuf[1 + shift:])

        stack.append(lexbuf[0])
        return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[1:])


print(parse_expr(0, 0, 0, [], lexer.lex("-100 ** 3 + - 200 * -400 * -600 + 300")))
