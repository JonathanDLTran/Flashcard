import lexer
from copy import deepcopy

UNOP_PRECEDENCE = 4
START_PRECEDENCE = 1
N_PRECEDENCE_LEVELS = 4

PRECENDENCE_MAP = {
    lexer.PLUS: 1,
    lexer.MINUS: 1,
    lexer.TIMES: 2,
    lexer.DIV: 2,
    lexer.EXP: 3,
}


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


class AssignVariableException(Exception):
    def __init__(self, str):
        pass


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

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(IntValue: " + str(self.value) + ")"


class VarValue(Expr):
    """
    IntValue represents an Variable Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

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

    def get_bop(self):
        return self.bop

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

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

    def get_unop(self):
        return self.unop

    def get_expr(self):
        return self.expr

    def __repr__(self):
        return "(UNOP: " + str(self.unop) + str(self.expr) + ")"


class Assign(Expr):
    """
    assign represents var assign expre
    """

    def __init__(self, var, expr=None):
        super().__init__()
        self.var = var
        self.expr = expr

    def set_expr(self, expr):
        self.expr = expr

    def set_var(self, var):
        self.var = var

    def get_expr(self):
        return self.expr

    def get_var(self):
        return self.var

    def __repr__(self):
        return "(Assign: " + str(self.var) + " := " + str(self.expr) + ")"


class While(Expr):
    """
    While represents
    while guard_expr dowhile
        phrases
    endwhile
    """

    def __init__(self, guard=None, body_list=None):
        super().__init__()
        self.guard = guard
        self.body = body_list

    def set_guard(self, guard):
        self.guard = guard

    def set_body(self, body_list):
        self.body = body_list

    def get_guard(self):
        return self.guard

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(while " + str(self.guard) + " dowhile\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendwhile)"


class For(Expr):
    """
    For represents
    For var from int to int by int dofor
        phrases
    endfor
    """

    def __init__(self, index, from_int, end_int, by, body_list):
        super().__init__()
        self.index = index
        self.from_int = from_int
        self.end_int = end_int
        self.by = by
        self.body = body_list

    def __repr__(self):
        return "(for " + str(self.index) + " from " + str(self.from_int) + " to " + str(self.end_int) + " by " + str(self.by) + " dofor\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendfor)"


class Function(Expr):
    """
    Function represents
    fun f a b c ->
        body
    endfun
    """

    def __init__(self, name, args_list, body_list):
        super().__init__()
        self.name = name
        self.args = args_list
        self.body = body_list

    def __repr__(self):
        return "(fun " + str(self.name) + " " + " ".join(list(map(lambda arg: str(arg), self.args))) + " ->\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendfun)"


class IfThenElse(Expr):
    """
    IFThenElse represents an if then else erpression
    """

    def __init__(self, if_guard, if_body, elif_guards=[], elif_bodies=[], else_body=None):
        super().__init__()
        self.if_pair = (if_guard, if_body)
        self.elif_list = (elif_guards, elif_bodies)
        self.else_body = else_body

    def __repr__(self):
        (if_guard, if_body) = self.if_pair
        elif_guards, elif_bodies = self.elif_list
        else_body = self.else_body
        return ("(if " + str(if_guard) + " then\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), if_body))) + "\nendif\n"
                + ("" if elif_guards == [] else "\n".join(list(map(lambda g, b: "elif " + str(g) + " then\n\t" +
                                                                   "\n\t".join(list(map(lambda phrase: str(phrase), b))) + "\nendelif\n", elif_guards, elif_bodies))))
                + ("" if else_body == None else "else\n\t" +
                   "\n\t".join(list(map(lambda phrase: str(phrase), else_body))) + "\nendelse\n")
                + ")"
                )


class Apply(Expr):
    """
    Apply represents fun (arg1 arg2...) with possibly no args as in
    fun () , with only open and close brackets.
    """

    def __init__(self, fun, args_list=[]):
        super().__init__()
        self.fun = fun
        self.args_list = args_list

    def set_args(self, args_list):
        self.args_list = args_list

    def get_fun(self):
        return self.fun

    def get_args(self):
        return self.args_list

    def __repr__(self):
        return "(Apply: " + str(self.fun) + "(" + (" ".join(list(map(lambda a: str(a), self.args_list)))) + ")" + ")"


class Return(Expr):
    """
    return represents
    return expr;
    """

    def __init__(self, body):
        super().__init__()
        self.body = body

    def __repr__(self):
        return "(Return: " + str(self.body) + ";)"


class Program(Expr):
    """
    Program represents a syntacucally valid program
    """

    def __init__(self, phrase_list=[]):
        super().__init__()
        self.phrases = phrase_list

    def __repr__(self):
        return "(Program:\n" + "\n".join(list(map(lambda phrase: str(phrase), self.phrases))) + "\n)"


def reduce_stack(precedence, stack):
    """
    reduce_stack(stack) reduces the stack from the top of the stack
    to the end into a unified AST at precedence level precedence

    REQUIRES: [precendence] cannot be 0
    REQUIRES: [precendence] is psoitive
    REQUIRES: STACK is NOT EMPTY
    REQUIRES: STACK MUST BE ABLE TO TURNED INTO A VALID AST, E>G> A STACK WITH ONE ELEMENT
    MUST BE A VALUE OR VARIABLE!
    If the stack has one element, returns that element
    """
    assert precedence > 0
    if stack == []:
        return stack

    l = len(stack)
    if l == 1:
        return stack[0]

    if precedence <= 3:
        end_stack = stack[:3]
        bop = end_stack[1][1]
        start = end_stack[0]
        end = end_stack[2]
        new_stack = stack[3:]
        new_stack.insert(0, Bop(bop, start, end))
        return reduce_stack(precedence, new_stack)

    # -------- WILL BE DEPRECATED -------------
    # elif precedence == 4:
    #     unop = stack[0][1]
    #     val = stack[1]
    #     new_stack = stack[2:]
    #     new_stack.insert(0, Unop(unop, val))
    #     return reduce_stack(precedence, new_stack)


def get_precedence(symbol, precendence_map=PRECENDENCE_MAP):
    """
    get_precedence(symbol, precendence_map=PRECENDENCE_MAP) is the
    precendence of a symbol

    REQUIRES: precendence_map is a correct PRECENDENCE_MAP
    REQUIRES: SYMBOL is an OPERATOR in precendence_map
    """
    return precendence_map[symbol]


def get_between_brackets(lexbuf, idx):
    """
    get_between_brackets(lexbuf, idx) gets elements in lexbuf from idx
    that starts with a LPARENt e.g, '('
    We assume that idx is the poisition after the LPAREN in lexbuf
    Returns the length of the exprtems including start and end parentheses and
    list of the expr terms in lexbuf not including the start
    and end parentheses as a 2-tuple
    """
    stack = []
    stack.append(lexer.LPAREN)
    expr_terms = []
    i = idx

    while (i < len(lexbuf) and stack != []):

        typ, val = lexbuf[i]
        if val == lexer.LPAREN:
            stack.append(val)
        elif val == lexer.RPAREN:
            if stack != [] and stack[-1] == lexer.LPAREN:
                stack.pop()
        expr_terms.append((typ, val))
        i += 1

    if i > len(lexbuf):
        raise MissingParens("Missing or Misplaced Parentheses")
    if stack != []:
        raise MissingParens("Missing or Misplaced Parentheses")
    l = len(expr_terms)
    expr_terms.pop()  # remove last parentheses
    return (l, expr_terms)


def get_function_args(lexbuf, demarcation):
    """
    get_function_args(lexbuf, demarcation) gets the function arguments
    in lexbuf, as separated by demarcation characters

    REQUIRES: args can  have demarcation chracters inside of them,
    but they must be separated by parentheses, e.g.
    if comma "," is the demarcation between args,
    then f(g, h(3, 4)) is legal since the demarcation in inner function call
    h is separated by parens

    Raises MissingParens("lexbuf missing right parens") if a parens
    on the right is missing (not closed parens)
    """
    def get_function_args_helper(lexbuf, demarcation, stack, arg, args_list):
        if lexbuf == []:
            if arg != []:
                args_list.append(arg)
            return args_list

        pair = lexbuf[0]
        _, val = pair
        rem = lexbuf[1:]

        if stack == [] and val == demarcation:
            args_list.append(arg)
            return get_function_args_helper(rem, demarcation, stack, [], args_list)

        if val == lexer.LPAREN:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer.RPAREN:
            if len(stack) >= 1:
                if stack[0] == lexer.LPAREN:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens("lexbuf missing right parens")

        else:
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

    return get_function_args_helper(lexbuf, demarcation, [], [], [])


def lookahead(lexbuf, pos):
    """
    lookahead(lexbuf, pos) tells the precendence of the OPERATOR! at the lookeahad
    position [pos] in [lexbuf]

    Returns pair of op and precedence

    REQUIRES: lexbuf[pos] is an operator
    REQUIRES: pos in lexbuf!
    """
    op = lexbuf[pos]
    symbol = op[1]
    assert symbol in lexer.OPERATIONS
    return op, get_precedence(symbol, PRECENDENCE_MAP)


def match_elt(lexbuf):
    """
    match_elt(lexbuf) is the length of the element and the element object
    e.g. 1, Integer(1)
    or 3, Bop(...)

    if RPAREN is first character, will raise unmatched parentheses erro

    REQUIRES: 0th element is in lexbuf: len(lexbuf )> 1
    REQUIRES: elt is 0th element in lexbuf
    """
    elt_typ, elt_val = lexbuf[0]
    if elt_typ == lexer.INTEGER:
        return 1, IntValue(elt_val)
    elif elt_typ == lexer.VARIABLE:
        if len(lexbuf) > 1:
            _, la_val = lexbuf[1]
            if la_val == lexer.LPAREN:
                length, middle_terms = get_between_brackets(lexbuf, 2)
                split_args = get_function_args(middle_terms, lexer.COMMA)
                args_pairs = list(map(lambda args_buffer: parse_expr(
                    args_buffer), split_args))
                args = list(map(lambda pair: pair, args_pairs))
                return 2 + length, Apply(elt_val, args)
        return 1, VarValue(elt_val)
    elif elt_typ == lexer.KEYWORD and elt_val in lexer.UNOPS:
        # length, unop_val_ast = parse_expr(
        #     lexbuf[1:])
        # add in later provisions for parens to follow
        length, unop_val_ast = 1, lexbuf[1]
        return (1 + length), Unop(elt_val, unop_val_ast)
    elif elt_val == lexer.LPAREN:
        length, middle_terms = get_between_brackets(lexbuf, 1)
        parens_ast = parse_expr(middle_terms)
        return (1 + length), parens_ast
    elif elt_val == lexer.RPAREN:
        raise UnmatchedParenError(
            "Unmatched right parenthesis %s" % (elt_val))


def is_elt(pair):
    """
    is_elt(pair) is True iff pair is a elxer.Integer, Variabl;e, Keyword, Lparen
    rParen

    pair si 2 tuple from the lexer lexbuf list
    """
    elt_typ, elt_val = pair
    if elt_typ == lexer.INTEGER:
        return True
    elif elt_typ == lexer.VARIABLE:
        return True
    elif elt_typ == lexer.KEYWORD and elt_val in lexer.UNOPS:
        return True
    elif elt_val == lexer.LPAREN:
        return True
    elif elt_val == lexer.RPAREN:
        return True
    return False


def is_op(pair):
    """
    is_op(pair) is True iff pair is a lexer Operation, incljuing binop or unops
    """
    _, elt_val = pair
    return elt_val in lexer.OPERATIONS


# def parse_expr(is_parse_op, count, precedence, stack, lexbuf):
#     # ----------- 0 tokens remaining = nothing more to parse ----------
#     # ----------- Used to escape if start call has 0 tokens  ----------
#     if lexbuf == []:
#         return (count, reduce_stack(precedence, stack))

#     if not is_parse_op:
#         elt_length, elt_ast = match_elt(lexbuf)
#         rem = lexbuf[elt_length:]

#         if len(rem) <= 1:
#             stack.append(elt_ast)
#             return (count + elt_length), reduce_stack(precedence, stack)

#         _, sym_precedence = lookahead(lexbuf, elt_length)
#         rem = lexbuf[elt_length + 1:]
#         if sym_precedence == precedence:
#             stack.append(elt_ast)
#             return parse_expr(not is_parse_op, count + elt_length, precedence, stack, rem)
#         elif sym_precedence > precedence:
#             new_stack = []
#             new_stack.append(elt_ast)
#             inner_parse_length, inner_ast = parse_expr(not is_parse_op,
#                                                        elt_length, sym_precedence, new_stack, rem)
#             rem = rem[inner_parse_length:]
#             # need to do a lookahead after parsing inner ast
#             # depended! on next operator ! stack.append(inner_ast)
#             return parse_expr(not is_parse_op, count + elt_length + inner_parse_length, precedence, stack, rem)
#         else:
#             stack.append(elt_ast)
#             return (count + elt_length), reduce_stack(precedence, stack)

#     else:
#         stack.append(lexbuf[0])
#         return parse_expr(not is_parse_op, count + 1, precedence, stack, lexbuf[1:])


# list of stacks
# [stack 1, stack 2, stack 3, stack 4....] with stack based on precedence level
# when a element is read, it is held until an operator is found
    # if no associated operator [e.g. the buffer terminates],>
    # add to the current precendence level parsing at
    # reduce stack
    # else wait until next operator:
    # if operator at same precendence lvel
    # add to current precendence level
    # continue parsing
    # elseif operator at lower precendence level:
    # add to current precedence level
    # reduce stack
    # else:
    # add to new higher precedence level stack
    # parse at that new level


def reduce_super_stack(stack):
    i = len(stack) - 1
    while i >= 0:
        substack = stack[i]
        if substack != []:
            reduced_substack = reduce_stack(i + 1, substack)
            if i != 0 and reduced_substack != []:
                stack[i - 1].append(reduced_substack)
                stack[i] = []
        i -= 1
    return reduce_stack(1, stack[0])


def parse_op(count, held_ast, precedence, stack, lexbuf):
    assert lexbuf != []

    op, sym_precedence = lookahead(lexbuf, 0)
    rem = lexbuf[1:]
    if sym_precedence == precedence:
        stack[sym_precedence - 1].append(held_ast)
        stack[sym_precedence - 1].append(op)
        return parse_expr_helper(count + 1, None, sym_precedence, stack, rem)
    elif sym_precedence > precedence:
        stack[sym_precedence - 1].append(held_ast)
        stack[sym_precedence - 1].append(op)
        ast_length, higher_precedence_ast = parse_expr_helper(
            0, None, sym_precedence, stack, rem)
        rem = rem[ast_length:]
        if rem != []:
            return parse_op(count + ast_length + 1, higher_precedence_ast, precedence, stack, rem)
        # stack[precedence - 1].append(higher_precedence_ast)
        # stack[sym_precedence - 1] = []
        return (count + 1), reduce_super_stack(stack)
    else:
        finished_stack = stack[precedence - 1]
        finished_stack.append(held_ast)
        reduced_ast = reduce_stack(precedence, finished_stack)
        stack[precedence - 1] = []
        stack[sym_precedence - 1].append(reduced_ast)
        stack[sym_precedence - 1].append(op)

        return parse_expr_helper(count + 1, None, sym_precedence, stack, rem)


def parse_expr_helper_2(count, held_ast, precedence, stack, lexbuf):
    if lexbuf == []:
        return reduce_super_stack(stack)

    pair = lexbuf[0]

    if is_elt(pair):
        elt_length, elt_ast = match_elt(lexbuf)
        rem = lexbuf[elt_length:]
        if rem != []:
            return (count + elt_length), parse_op((count + elt_length), elt_ast, precedence, stack, rem)
        stack[precedence - 1].append(elt_ast)
        # substack = stack[precedence - 1]
        return (count + elt_length), reduce_super_stack(stack)
        # return (count + elt_length), reduce_stack(precedence, substack)


def fold_stack(stack):
    def fold_stack_helper(stack, fold_item):
        if len(stack) == 0:
            return stack
        if len(stack) == 1:
            l = len(stack)
            if fold_item != []:
                stack[l - 1].append(fold_item)
            reduced_ast = reduce_stack(l, stack[l - 1])
            return reduced_ast
        l = len(stack)
        if fold_item != []:
            stack[l - 1].append(fold_item)
        reduced_ast = reduce_stack(l, stack[l - 1])
        new_stack = deepcopy(stack[:(l-1)])
        return fold_stack_helper(new_stack, reduced_ast)
    return fold_stack_helper(stack, [])


def parse_expr_helper(lexbuf):
    stack = [[] for _ in range(N_PRECEDENCE_LEVELS)]
    precendence = 1
    l = len(lexbuf)
    carry_ast = None
    i = 0
    while (i < l):
        elt = carry_ast
        if carry_ast != None:
            elt = carry_ast
            rem = lexbuf[i:]
            elt_length = 0
        else:
            elt_length, elt = match_elt(lexbuf[i:])
            rem = lexbuf[i + elt_length:]

        if rem == []:
            stack[precendence - 1].append(elt)
            reduced_ast = reduce_stack(precendence, stack[precendence - 1])
            i += elt_length
            stack[precendence - 1] = [reduced_ast]
            stack = fold_stack(stack)
        else:
            op = rem[0]  # if it exists
            _, op_val = op

            op_prec = get_precedence(op_val, PRECENDENCE_MAP)

            if op_prec == precendence:
                stack[op_prec - 1].append(elt)
                stack[op_prec - 1].append(op)
                i += elt_length + 1

            elif op_prec > precendence:
                stack[op_prec - 1].append(elt)
                stack[op_prec - 1].append(op)
                i += elt_length + 1
                precendence = op_prec

            else:  # op_prec < precendence:
                stack[precendence - 1].append(elt)
                lower_ast = reduce_stack(precendence, stack[precendence - 1])
                stack[precendence - 1] = []
                stack[op_prec - 1].append(lower_ast)
                stack[op_prec - 1].append(op)
                i += elt_length + 1  # skip operator and redo on next run
                precendence = op_prec
    return stack


def parse_expr(lexbuf):
    return parse_expr_helper(lexbuf)
    # start_stack = [[] for _ in range(N_PRECEDENCE_LEVELS)]
    # return parse_expr_helper(0, None, START_PRECEDENCE, start_stack, lexbuf)

# driving code
# starting stack list is [[] for _ in range(N_PRECEDENCE_LEVELS)]
# starting precedence is 1
# starting buffer is lexbuf
# not tracking count anymore, just track releative position in each buffer
# held_ast is None
# count is 0


if __name__ == "__main__":
    print(parse_expr(lexer.lex("3")))
    print(parse_expr(lexer.lex("3 + 4")))
    print(parse_expr(lexer.lex("3 + 4 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + 5 + 6")))

    print(parse_expr(lexer.lex("-3")))
    print(parse_expr(lexer.lex("-3 + 4")))
    print(parse_expr(lexer.lex("-3 + -4")))
    print(parse_expr(lexer.lex("3 + -4")))
    print(parse_expr(lexer.lex("-3 + 4 + 6")))
    print(parse_expr(lexer.lex("3 + -4 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + -6")))
    print(parse_expr(lexer.lex("3 + -4 + -6")))
    print(parse_expr(lexer.lex("-3 + -4 + 6")))
    print(parse_expr(lexer.lex("-3 + 4 + -6")))
    print(parse_expr(lexer.lex("-3 + -4 + -6")))
    print(parse_expr(lexer.lex("-3 + 4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + -5 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + 5 + -6")))
    print(parse_expr(lexer.lex("-3 + -4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 + -5 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + -5 + -6")))
    print(parse_expr(lexer.lex("-3 + 4 + 5 + -6")))
    print(parse_expr(lexer.lex("3 + -4 + 5 + -6")))
    print(parse_expr(lexer.lex("3 + -4 + -5 + 6")))

    print(parse_expr(lexer.lex("(3)")))
    print(parse_expr(lexer.lex("(((3)))")))
    print(parse_expr(lexer.lex("(3 + 4)")))
    print(parse_expr(lexer.lex("3 + (4 + 6)")))
    print(parse_expr(lexer.lex("(3 + 4 + 6)")))
    print(parse_expr(lexer.lex("(3 + 4) + 6")))
    print(parse_expr(lexer.lex("(3) + 4 + 5 + 6")))
    print(parse_expr(lexer.lex("(3) + (4 + 5) + 6")))
    print(parse_expr(lexer.lex("((3) + (4 + 5)) + 6")))
    print(parse_expr(lexer.lex("(3) + ((4 + 5) + 6)")))

    print(parse_expr(lexer.lex("(-3)")))
    print(parse_expr(lexer.lex("(((-3)))")))
    print(parse_expr(lexer.lex("(3 + -4)")))
    print(parse_expr(lexer.lex("(-3 + -4)")))
    print(parse_expr(lexer.lex("-3 + (4 + 6)")))
    print(parse_expr(lexer.lex("-3 + (-4 + 6)")))
    print(parse_expr(lexer.lex("-3 + (-4 + -6)")))
    print(parse_expr(lexer.lex("3 + (-4 + 6)")))
    print(parse_expr(lexer.lex("3 + (4 + -6)")))
    print(parse_expr(lexer.lex("3 + (-4 + -6)")))
    print(parse_expr(lexer.lex("(3 + 4 + 6)")))
    print(parse_expr(lexer.lex("(3 + 4) + 6")))
    print(parse_expr(lexer.lex("(-3 + 4 + 6)")))
    print(parse_expr(lexer.lex("(-3 + -4) + -6")))
    print(parse_expr(lexer.lex("(3) + 4 + 5 + 6")))
    print(parse_expr(lexer.lex("(3) + (4 + 5) + 6")))
    print(parse_expr(lexer.lex("((3) + (4 + 5)) + 6")))
    print(parse_expr(lexer.lex("(3) + ((-4 + 5) + 6)")))
    print(parse_expr(lexer.lex("(3) + ((-4 + -5) + 6)")))
    print(parse_expr(lexer.lex("(3) + ((4 + -5) + 6)")))
    print(parse_expr(lexer.lex("(3) + ((-4 + -5) + -6)")))

    print(parse_expr(lexer.lex("3 * 4")))
    print(parse_expr(lexer.lex("3 * 4 + 6")))
    print(parse_expr(lexer.lex("3 + 4 * 6")))
    print(parse_expr(lexer.lex("3 * 4 * 6")))
    print(parse_expr(lexer.lex("3 * 4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + 4 * 5 + 6")))
    print(parse_expr(lexer.lex("3 + 4 + 5 * 6")))
    print(parse_expr(lexer.lex("3 + 4 * 5 * 6")))
    print(parse_expr(lexer.lex("3 * 4 * 5 + 6")))
    print(parse_expr(lexer.lex("3 * 4 + 5 * 6")))
    print(parse_expr(lexer.lex("3 * 4 * 5 * 6")))

    print(parse_expr(lexer.lex("-3 * 4")))
    print(parse_expr(lexer.lex("-3 * -4")))
    print(parse_expr(lexer.lex("3 * -4")))
    print(parse_expr(lexer.lex("-3 * -4 + 6")))
    print(parse_expr(lexer.lex("-3 + 4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 * -5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 + 5 * -6")))
    print(parse_expr(lexer.lex("-3 + -4 * -5 * -6")))
    print(parse_expr(lexer.lex("-3 * -4 * -5 + -6")))
    print(parse_expr(lexer.lex("-3 * -4 + -5 * -6")))
    print(parse_expr(lexer.lex("3 * -4 * -5 * -6")))

    print(parse_expr(lexer.lex("-3 * 4")))
    print(parse_expr(lexer.lex("-3 ** -4")))
    print(parse_expr(lexer.lex("3 * -4")))
    print(parse_expr(lexer.lex("-3 * -4 + 6")))
    print(parse_expr(lexer.lex("-3 + 4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 * -5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 + 5 * -6")))
    print(parse_expr(lexer.lex("-3 + -4 * -5 * -6")))
    print(parse_expr(lexer.lex("-3 * -4 * -5 + -6")))
    print(parse_expr(lexer.lex("-3 * -4 + -5 ** -6")))
    print(parse_expr(lexer.lex("3 ** -4 ** -5 * -6")))

    print(parse_expr(lexer.lex("unary()")))
    print(parse_expr(lexer.lex("f(1, 2 + 3)")))
    print(parse_expr(lexer.lex("f(g(3, 4), h(g(9), 8))")))

    print(parse_expr(lexer.lex("-x * 4")))
    print(parse_expr(lexer.lex("-3 ** -y")))
    print(parse_expr(lexer.lex("3 * -4")))
    print(parse_expr(lexer.lex("-3 * -4 + 6")))
    print(parse_expr(lexer.lex("-3 + 4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 * 6")))
    print(parse_expr(lexer.lex("3 * -4 + 5 + 6")))
    print(parse_expr(lexer.lex("3 + -4 * -5 + 6")))
    print(parse_expr(lexer.lex("x + -4 + 5 * -6")))
    print(parse_expr(lexer.lex("-3 + -4 * -5 * -6")))
    print(parse_expr(lexer.lex("-3 * -y * -z + -6")))
    print(parse_expr(lexer.lex("-3 * -4 + -5 ** -6")))
    print(parse_expr(lexer.lex("3 ** -4 ** -k * -6")))

    # print(parse_expr(lexer.lex("3 * 4")))
    # print(parse_expr(lexer.lex("-3")))
    # print(parse_expr(lexer.lex("-3 * -4")))
    # print(parse_expr(lexer.lex("3 + 4 * 2")))
    # print(parse_expr(lexer.lex("3 * 4 + 2")))
    # print(parse_expr(lexer.lex("3 * 4 * 2")))
    # print(parse_expr(lexer.lex("3 * 4 * 2 + 2 * 3 + 1 * 2 * 3")))
