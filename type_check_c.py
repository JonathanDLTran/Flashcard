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


def check_var(var, ctx):
    """
    check_var(var, ctx) returns the correct type for a var expression
    in ctx, otherwise raises error
    """
    assert type(var) == ast_generator_c.VarValue
    var_str = var.get_value()
    if var_str in ctx:
        return ctx[var_str]
    raise TypeError(f"Unbound Type for Variable : {var_str}")


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
    typ_node = declr.get_typ()
    typ = typ_node.get_typ()

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
    return ctx


if __name__ == "__main__":
    program = 'str s1 := "hello"; str s2 := s1; int x := 3; int y := 4; x := y; y := 5; x := x + y; bool b1 := True; bool b2 := False; int z := -3; int w := x + y - z * z;'
    result = type_check(ast_generator_c.parse_program(lexer_c.lex(program)))
    print(result)
