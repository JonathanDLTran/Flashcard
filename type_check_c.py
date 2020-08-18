"""
type_check_c is a type checking module to evaluate the type correctness
of a c-like language defined in lexer_c and ast_generator_c
"""


# ---------- ADDITIONAL IMPORTS -----------------
from copy import deepcopy


# --------- LANGUAGE DEPENDENT IMPORTS ----------
import ast_generator_c
import lexer_c


# --------- RETURN EXCEPTION --------------------
class ReturnException(Exception):
    """
    ReturnException(Exception) is an exception hpolding information
    regarding the return type
    """

    def __init__(self, ret_typ):
        """
        __init__(self, ret_typ) creates a return exception 
        with return type ret_typ
        """
        super().__init__()
        self.ret_type = ret_typ

    def get_ret_type(self):
        """
        get_ret_type(self) os the return type of the exception
        """
        return self.ret_type


def check_int(int_val, ctx):
    """
    check_int(int_val, ctx)returns the correct type for a int expression
    in ctx, otherwise raises error
    """
    assert type(int_val) == ast_generator_c.IntValue
    return ast_generator_c.IntType()


def check_bool(bool_val, ctx):
    """
    check_bool(bool_val, ctx) returns the correct type for a bool expression
    in ctx, otherwise raises error
    """
    assert type(bool_val) == ast_generator_c.BoolValue
    return ast_generator_c.BoolType()


def check_str(str_val, ctx):
    """
    check_str(str_val, ctx) returns the correct type for a str expression
    in ctx, otherwise raises error
    """
    assert type(str_val) == ast_generator_c.StrValue
    return ast_generator_c.StrType()


def check_float(float_val, ctx):
    """
    check_str(str_val, ctx) returns the correct type for a str expression
    in ctx, otherwise raises error
    """
    assert type(float_val) == ast_generator_c.FloatValue
    return ast_generator_c.FloatType()


def check_var(var, ctx):
    """
    check_var(var, ctx) returns the correct type for a var expression
    in ctx, otherwise raises error
    """
    assert type(var) == ast_generator_c.VarValue
    var_str = var.get_value()
    if var_str in ctx:
        return ctx[var_str]
    raise UnboundLocalError(f"Unbound Type for Variable : {var_str}")


def check_tuple(tup, ctx):
    """
    check_tuple(tup, ctx) returns the correct type for a tup expression
    in ctx, otherwise raises error
    """
    assert type(tup) == ast_generator_c.Tuple
    exprs_list = tup.get_exprs()
    tup_component_types = []
    for expr in exprs_list:
        expr_typ = check_expr(expr, ctx)
        tup_component_types.append(expr_typ)
    return ast_generator_c.TupleType(tup_component_types)


def check_list(lst, ctx):
    """
    check_list(lst, ctx) returns the correct type for a lst expression
    in ctx, otherwise raises error
    """
    assert type(lst) == ast_generator_c.List
    exprs_list = lst.get_exprs()
    lst_component_types = []
    for expr in exprs_list:
        expr_typ = check_expr(expr, ctx)
        lst_component_types.append(expr_typ)
    if lst_component_types == []:
        return ast_generator_c.WildcardType()
    first_type = lst_component_types[0]
    for typ in lst_component_types:
        if typ != first_type:
            raise TypeError(
                f"Type mismatch in list: first element type is {first_type} and one of the elements has a mismatched type {typ}. ")
    return ast_generator_c.ListType(first_type)


def check_unop(unop, ctx):
    """
    check_unop(unop, ctx) returns the correct type for a unop expression
    in ctx, otherwise raises error
    """
    assert type(unop) == ast_generator_c.Unop
    expr = unop.get_expr()
    op = unop.get_unop()

    typ_e = check_expr(expr, ctx)

    if op in [lexer_c.MINUS]:
        if typ_e == ast_generator_c.IntType():
            return ast_generator_c.IntType()
        elif typ_e == ast_generator_c.FloatType():
            return ast_generator_c.FloatType()
        raise TypeError(
            f"Type mismatch for int or float unary operator: expression type is {typ_e} and the operator {op} requires the expression to be an int. ")

    elif op in [lexer_c.NOT]:
        if typ_e == ast_generator_c.BoolType():
            return ast_generator_c.BoolType()
        raise TypeError(
            f"Type mismatch for bool unary operator: expression type is {typ_e} and the operator {op} requires the expression to be a bool. ")

    raise RuntimeError("Unimplemented")


def check_bop(bop, ctx):
    """
    check_bop(bop, ctx) returns the correct type for a bop expression
    in ctx, otherwise raises error
    """
    assert type(bop) == ast_generator_c.Bop
    left = bop.get_left()
    op = bop.get_bop()
    right = bop.get_right()

    typ_l = check_expr(left, ctx)
    typ_r = check_expr(right, ctx)

    if op in [lexer_c.PLUS, lexer_c.MINUS, lexer_c.TIMES, lexer_c.DIV]:
        if typ_l == ast_generator_c.IntType() and typ_r == ast_generator_c.IntType():
            return ast_generator_c.IntType()
        raise TypeError(
            f"Type mismatch for int binary operator: left type is {typ_l}, right type is {typ_r} and the operator {op} requires both to be ints. ")

    elif op in [lexer_c.AND, lexer_c.OR]:
        if typ_l == ast_generator_c.BoolType() and typ_r == ast_generator_c.BoolType():
            return ast_generator_c.BoolType()
        raise TypeError(
            f"Type mismatch for bool binary operator: left type is {typ_l}, right type is {typ_r} and the operator {op} requires both to be bools. ")

    elif op in [lexer_c.CONCAT]:
        if typ_l == ast_generator_c.StrType() and ast_generator_c.StrType():
            return ast_generator_c.StrType()
        raise TypeError(
            f"Type mismatch for str binary operator: left type is {typ_l}, right type is {typ_r} and the operator {op} requires both to be strings. ")

    raise RuntimeError("Unimplemented")


def check_expr(expr, ctx):
    """
    check_expr(expr) is the type of the expr if it is well-typed,
    otherwise raises exception
    """
    assert (isinstance(expr, ast_generator_c.Expr))
    if type(expr) == ast_generator_c.IntValue:
        return check_int(expr, ctx)
    elif type(expr) == ast_generator_c.BoolValue:
        return check_bool(expr, ctx)
    elif type(expr) == ast_generator_c.VarValue:
        return check_var(expr, ctx)
    elif type(expr) == ast_generator_c.StrValue:
        return check_str(expr, ctx)
    elif type(expr) == ast_generator_c.FloatValue:
        return check_float(expr, ctx)
    elif type(expr) == ast_generator_c.Tuple:
        return check_tuple(expr, ctx)
    elif type(expr) == ast_generator_c.List:
        return check_list(expr, ctx)
    elif type(expr) == ast_generator_c.Unop:
        return check_unop(expr, ctx)
    elif type(expr) == ast_generator_c.Bop:
        return check_bop(expr, ctx)
    raise RuntimeError("Unimplemented")


def check_declaration(declr, ctx):
    """
    check_declaration(declr, ctx) is the tontext of the declaraction
    after the declaration is updated, otherwise raises error if incorrect typed
    """
    assert type(declr) == ast_generator_c.Declaration
    assignment_node = declr.get_assign()
    var = assignment_node.get_var()
    typ = declr.get_typ()

    if var not in ctx:
        ctx[var] = typ
    else:
        original_typ = ctx[var]
        raise TypeError(
            f"Cannot reassign variable to different type: Original Type was {original_typ} while new type is {typ}")

    ctx = check_assignment(assignment_node, ctx)
    return ctx


def check_assignment(assign, ctx):
    """
    check_assignment(assign, ctx) is the tontext of the assignment
    after the assingment is executed, otherwise raises error if incorrect typed
    """
    assert type(assign) == ast_generator_c.Assign
    var = assign.get_var()
    expr = assign.get_expr()

    expr_typ = check_expr(expr, ctx)
    if var in ctx:
        var_typ = ctx[var]
    else:
        raise UnboundLocalError(f"Unbound Type for Variable : {var}")

    if expr_typ == var_typ:
        return ctx
    else:
        raise TypeError(
            f"Assignment to variable does match variable type: Variable {var} has type {var_typ} while the assignment has type {expr_typ}. ")


def check_declare_tuple(tup, ctx):
    """
    check_declare_tuple(phrase, ctx)  checks if the declaration of the tuple type checks
    otherwise raises exceptiion
    """
    assert type(tup) == ast_generator_c.DeclareTuple
    tup_typ = tup.get_typ()
    assign = tup.get_assign()
    var = assign.get_var()

    if var not in ctx:
        ctx[var] = tup_typ
    else:
        original_typ = ctx[var]
        raise TypeError(
            f"Cannot reassign variable to different type: Original Type was {original_typ} while new type is {tup_typ}")

    ctx = check_assignment(assign, ctx)
    return ctx


def check_declare_list(lst, ctx):
    """
    check_declare_list(lst, ctx) checks if the declaration of the list type
    type checks otherwise raises exception
    """
    assert type(lst) == ast_generator_c.DeclareList
    lst_typ = lst.get_typ()
    assign = lst.get_assign()
    var = assign.get_var()

    if var not in ctx:
        ctx[var] = lst_typ
    else:
        original_typ = ctx[var]
        raise TypeError(
            f"Cannot reassign variable to different type: Original Type was {original_typ} while new type is {lst_typ}")

    ctx = check_assignment(assign, ctx)
    return ctx


def check_declare_function(func, ctx):
    """
    check_declare_function(func, ctx) verifies the reutrn type of the function
    matches the function inputs and declared output, and adds it to the
    context, otherwise raises error
    """
    raise RuntimeError("Unimplemented")


def check_declare_for(_for, ctx):
    """
    check_declare_for(_for, ctx) checks if a for loop type checks
    or raises an error
    """
    for_ctx = deepcopy(ctx)
    index = _for.get_index().get_value()
    for_ctx[index] = lexer_c.INT  # always bind index to an int in only forctx
    _from = _for.get_from()
    _end = _for.get_end()
    _by = _for.get_by()
    body = _for.get_body()

    from_typ = check_expr(_from, ctx)
    end_typ = check_expr(_end, ctx)
    by_typ = check_expr(_by, ctx)

    if from_typ != ast_generator_c.IntType():
        raise TypeError("For loop From must be an Int")

    if end_typ != ast_generator_c.IntType():
        raise TypeError("For loop End must be an Int")

    if by_typ != ast_generator_c.IntType():
        raise TypeError("By loop End must be an Int")

    for phrase in body:
        for_ctx = check_phrase(phrase, for_ctx)

    # return original context
    return ctx


def check_declare_while(_while, ctx):
    """
    check_declare_while(_while, ctx checkcks a while loop or raises
    an exception
    """
    guard = _while.get_guard()
    body = _while.get_body()

    guard_typ = check_expr(guard, ctx)
    if type(guard_typ) == str and guard_typ != lexer_c.BOOL:
        raise TypeError("While loop Guard must be a Bool")

    while_ctx = deepcopy(ctx)
    for phrase in body:
        while_ctx = check_phrase(phrase, while_ctx)

    # return original context
    return ctx


def check_ignore(ignore, ctx):
    """
    check_ignore(ignore, ctx) type checks ignore and returns ctx
    otherwise raises exception
    """
    expr = ignore.get_expr()
    _ = check_expr(expr, ctx)  # ignore type
    return ctx


def check_ifthenelse(ifthenelse, ctx):
    """
    check_ifthenelse(phrase, ctx) type checks ifthenelse otherwise
    raises error
    """
    (if_guard, if_body) = ifthenelse.get_if_pair()
    (elif_guards, elif_bodies) = ifthenelse.get_elif_pair_list()
    else_body = ifthenelse.get_else()

    if_guard_typ = check_expr(if_guard, ctx)
    if type(if_guard_typ) == str and if_guard_typ != lexer_c.BOOL:
        raise TypeError("If statement Guard must be a Bool")

    if_body_ctx = deepcopy(ctx)
    for phrase in if_body:
        if_body_ctx = check_phrase(phrase, if_body_ctx)

    for guard in elif_guards:
        elif_guard_typ = check_expr(guard, ctx)
        if type(elif_guard_typ) == str and elif_guard_typ != lexer_c.BOOL:
            raise TypeError("Elif statement Guard must be a Bool")

    for elif_body in elif_bodies:
        elif_body_ctx = deepcopy(ctx)
        for phrase in elif_body:
            elif_body_ctx = check_phrase(phrase, elif_body_ctx)

    if else_body != None:
        else_ctx = deepcopy(ctx)
        for phrase in else_body:
            else_ctx = check_phrase(phrase, else_ctx)

    return ctx


def check_return(ret, ctx):
    """
    check_return(ret, ctx) type checks a return statement and raises
    a Return exception with the type, otherwise raises Type Exception
    """
    ret_body = ret.get_body()
    ret_type = check_expr(ret_body, ctx)
    raise ReturnException(ret_type)


def check_phrase(phrase, ctx):
    """
    check_phrase(phrase, ctx) type checks a phrase and returns ctx otherwise raises exception
    """
    if type(phrase) == ast_generator_c.Declaration:
        ctx = check_declaration(phrase, ctx)
    elif type(phrase) == ast_generator_c.Assign:
        ctx = check_assignment(phrase, ctx)
    elif type(phrase) == ast_generator_c.DeclareTuple:
        ctx = check_declare_tuple(phrase, ctx)
    elif type(phrase) == ast_generator_c.DeclareList:
        ctx = check_declare_list(phrase, ctx)
    elif type(phrase) == ast_generator_c.Function:
        ctx = check_declare_function(phrase, ctx)
    elif type(phrase) == ast_generator_c.For:
        ctx = check_declare_for(phrase, ctx)
    elif type(phrase) == ast_generator_c.While:
        ctx = check_declare_while(phrase, ctx)
    elif type(phrase) == ast_generator_c.Ignore:
        ctx = check_ignore(phrase, ctx)
    elif type(phrase) == ast_generator_c.IfThenElse:
        ctx = check_ifthenelse(phrase, ctx)
    elif type(phrase) == ast_generator_c.Return:
        check_return(phrase, ctx)
    else:
        raise RuntimeError("Unimplemented")
    return ctx


def type_check(program):
    """
    Returns the final context if the program type checks correctly else
    raises exception of type check error
    """
    assert type(program) == ast_generator_c.Program
    phrases = program.get_phrases()
    ctx = {}
    for phrase in phrases:
        ctx = check_phrase(phrase, ctx)
    return ctx


if __name__ == "__main__":
    program = 'if True then int m := 1; endif elif True then int n:= -2; endelif elif True then int n:= -2; endelif else int o := 24; endelse  ~1; ~2 + 3 - 4;  bool k := True; while k dowhile k := False; endwhile  for i from 1 + 1 to 3 by 1 dofor int j := 1; endfor ([int] * int) tl := (|[], 3|); tl := (|[2], -3|); [(int * int)] l1 := []; l1 := [(|1, 2|)]; l1 := []; l1 := [(|-1, -2|)]; [[int]] l := []; l := [[1, 2], [3]]; l := [[2]]; l := []; float f := -1.0; str s1 := "hello"; str s2 := s1; int x := 3; int y := 4; x := y; y := 5; x := x + y; bool b1 := True; bool b2 := False; int z := -3; int w := x + y - z * z; (int * int) t := (|1, 2|); (int * (str * int)) t2 := (|1, (|"hello", 3|)|); t := (| -1, -1|);'
    try:
        result = type_check(
            ast_generator_c.parse_program(lexer_c.lex(program)))
        print(result)
    except ReturnException as re:
        print(
            f"Return Exception caught: Return statements must be inside of function calls: Your return value of {re.get_ret_type()} was not nested in a function call.")
    # except Exception as e:
    #     print(e)

# union type is
# [|val|]
# union cash := [|int; float|]
# cash c := [|1|]
