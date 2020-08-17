"""
type_check_c is a type checking module to evaluate the type correctness
of a c-like language defined in lexer_c and ast_generator_c
"""


# --------- LANGUAGE DEPENDENT IMPORTS ----------
import ast_generator_c
import lexer_c


def check_int(int_val, ctx):
    """
    check_int(int_val, ctx)returns the correct type for a int expression
    in ctx, otherwise raises error
    """
    assert type(int_val) == ast_generator_c.IntValue
    return lexer_c.INT


def check_bool(bool_val, ctx):
    """
    check_bool(bool_val, ctx) returns the correct type for a bool expression
    in ctx, otherwise raises error
    """
    assert type(bool_val) == ast_generator_c.BoolValue
    return lexer_c.BOOL


def check_str(str_val, ctx):
    """
    check_str(str_val, ctx) returns the correct type for a str expression
    in ctx, otherwise raises error
    """
    assert type(str_val) == ast_generator_c.StrValue
    return lexer_c.STR


def check_float(float_val, ctx):
    """
    check_str(str_val, ctx) returns the correct type for a str expression
    in ctx, otherwise raises error
    """
    assert type(float_val) == ast_generator_c.FloatValue
    return lexer_c.FLOAT


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
        return ast_generator_c.WILDCARD_TYPE
    first_type = lst_component_types[0]
    # if first_type == ast_generator_c.WILDCARD_TYPE:
    #     raise TypeError(
    #         f"Type mismatch in list: first element type is {first_type} but a non-empty list cannot have type {ast_generator_c.WILDCARD_TYPE}. ")
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
        if typ_e == lexer_c.INT:
            return lexer_c.INT
        elif typ_e == lexer_c.FLOAT:
            return lexer_c.FLOAT
        raise TypeError(
            f"Type mismatch for int unary operator: expression type is {typ_e} and the operator {op} requires the expression to be an int. ")

    elif op in [lexer_c.NOT]:
        if typ_e == lexer_c.BOOL:
            return lexer_c.BOOL
        raise TypeError(
            f"Type mismatch for int unary operator: expression type is {typ_e} and the operator {op} requires the expression to be a bool. ")

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
        if typ_l == lexer_c.INT and typ_r == lexer_c.INT:
            return lexer_c.INT
        raise TypeError(
            f"Type mismatch for int binary operator: left type is {typ_l}, right type is {typ_r} and the operator {op} requires both to be ints. ")

    elif op in [lexer_c.AND, lexer_c.OR]:
        if typ_l == lexer_c.BOOL and typ_r == lexer_c.BOOL:
            return lexer_c.BOOL
        raise TypeError(
            f"Type mismatch for bool binary operator: left type is {typ_l}, right type is {typ_r} and the operator {op} requires both to be bools. ")

    elif op in [lexer_c.CONCAT]:
        if typ_l == lexer_c.STR and typ_r == lexer_c.STR:
            return lexer_c.STR
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
    # typ_node = declr.get_typ()
    typ = declr.get_typ()
    # typ = typ_node.get_typ()

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


def type_check(program):
    """
    Returns the final context if the program type checks correctly else
    raises exception of type check error
    """
    assert type(program) == ast_generator_c.Program
    phrases = program.get_phrases()
    ctx = {}
    for phrase in phrases:
        if type(phrase) == ast_generator_c.Declaration:
            ctx = check_declaration(phrase, ctx)
        elif type(phrase) == ast_generator_c.Assign:
            ctx = check_assignment(phrase, ctx)
        elif type(phrase) == ast_generator_c.DeclareTuple:
            ctx = check_declare_tuple(phrase, ctx)
        elif type(phrase) == ast_generator_c.DeclareList:
            ctx = check_declare_list(phrase, ctx)
        else:
            raise RuntimeError("Unimplemented")
    return ctx


if __name__ == "__main__":
    program = '([int] * int) tl := (|[], 3|); tl := (|[2], -3|); [(int * int)] l1 := []; l1 := [(|1, 2|)]; l1 := []; l1 := [(|-1, -2|)]; [[int]] l := []; l := [[1, 2], [3]]; l := [[2]]; l := []; float f := -1.0; str s1 := "hello"; str s2 := s1; int x := 3; int y := 4; x := y; y := 5; x := x + y; bool b1 := True; bool b2 := False; int z := -3; int w := x + y - z * z; (int * int) t := (|1, 2|); (int * (str * int)) t2 := (|1, (|"hello", 3|)|); t := (| -1, -1|);'
    try:
        result = type_check(
            ast_generator_c.parse_program(lexer_c.lex(program)))
        print(result)
    except Exception as e:
        print(e)


# lists are declared [type] var := list
# e.g. [int] ages := [1, 2, 3];
# or [[int]] age_lists := [[1], [2, 3]]
# where the second imples that each element of the list is itself a list
