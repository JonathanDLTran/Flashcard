import lexer
import ast_generator
from copy import deepcopy


class InterpretError(Exception):
    def __init__(self, message):
        self.message = message


class ReturnException(Exception):
    def __init__(self, return_value):
        self.return_value = return_value

    def get_ret_value(self):
        return self.return_value


def interpret_expr(expr, env):
    if type(expr) == ast_generator.IntValue:
        return expr.get_value()
    elif type(expr) == ast_generator.VarValue:
        var_name = expr.get_value()
        if ("variable", var_name) not in env:
            raise InterpretError(str(var_name) + " not bound in program")
        return env[("variable", var_name)]
    elif type(expr) == ast_generator.Unop:
        unop = expr.get_unop()
        unop_expr = expr.get_expr()

        if unop == lexer.MINUS:
            return -1 * interpret_expr(unop_expr, env)
    elif type(expr) == ast_generator.Bop:
        bop = expr.get_bop()
        bop_left_expr = expr.get_left()
        bop_right_expr = expr.get_right()

        left = interpret_expr(bop_left_expr, env)
        right = interpret_expr(bop_right_expr, env)

        if bop == lexer.PLUS:
            return left + right
        elif bop == lexer.MINUS:
            return left - right
        elif bop == lexer.TIMES:
            return left * right
        elif bop == lexer.DIV:
            return left // right  # integer div
    elif type(expr) == ast_generator.Extern:
        return interpret_extern(expr, env)
    elif type(expr) == ast_generator.Apply:
        function_name = expr.get_fun()
        args_list = expr.get_args()
        args = list(map(lambda arg: interpret_expr(arg, env), args_list))

        function = env[("function", function_name)]
        function_body = function.get_body()
        function_params = function.get_args()
        params = list(map(lambda p: p.get_value(), function_params))

        if len(args) != len(function_params):
            raise InterpretError("Given args have different arity than function args: length of args is " +
                                 str(len(args)) + "!= length of params is " + str(len(function_params)))

        def assign_param(param, arg, env):
            env[param] = arg
        func_closure = deepcopy(env)
        _ = list(map(lambda arg, param: assign_param(
            param, arg, func_closure), args, params))

        try:
            pass
            # need to handle closures
            # return interpret_program(function_body, func_closure)
        except ReturnException as e:
            # return captured
            return e.get_ret_value()


def interpret_extern(expr, env):
    function_name = expr.get_fun()
    args_list = expr.get_args()
    args = list(map(lambda arg: interpret_expr(arg, env), args_list))

    if function_name == ast_generator.PRINT:
        print(*args)
        return 1  # print extern returns 1 if it occurred

    # other externs as needed, checking arg length
    # for example, len(), range(), is_int(), is_bool(), int(), str(),..
    pass


def interpret_phrase(phrase, env):
    if type(phrase) == ast_generator.Assign:
        variable = phrase.get_var()
        body_expr = phrase.get_expr()
        body_value = interpret_expr(body_expr, env)
        env[("variable", variable)] = body_value
        return env
    elif type(phrase) == ast_generator.While:
        guard_expr = phrase.get_guard()
        body_list = phrase.get_body()
        guard_value = interpret_expr(guard_expr, env)

        while guard_value:  # using truthy values including non zero ints
            # one loop
            for sub_phrase in body_list:
                env = interpret_phrase(sub_phrase, env)  # update env
            # recalculate guard at bottom of loop to see if it continues
            guard_value = interpret_expr(guard_expr, env)
        return env
    elif type(phrase) == ast_generator.IfThenElse:
        pass
    elif type(phrase) == ast_generator.For:
        pass
    elif type(phrase) == ast_generator.Return:
        # leave current env and do not save it
        raise ReturnException(phrase.get_body())
    elif type(phrase) == ast_generator.Ignore:
        expr = phrase.get_expr()
        _ = interpret_expr(expr, env)
        # do not bind as this is an ignore
        return env
    elif type(phrase) == ast_generator.Function:
        pass
        # TODO
        # function_name = phrase.get_name()
        # env[("function", function_name)] = phrase
        # return env

        # need to get closures


def interpret_program(program, env):
    phrase_list = program.get_phrases()
    for phrase in phrase_list:
        env = interpret_phrase(phrase, env)
    return env


def interpret(program):
    assert type(program) == ast_generator.Program
    return interpret_program(program, {})


print(ast_generator.parse_expr(
    lexer.lex("2 + -1 * (3 * 5) * 4 * 3 * 2 * 1 * 0 * -1"))
)
print(ast_generator.parse_expr(
    lexer.lex("2 + -1 * 3 * 5 * 4 * 3 * 2"))
)
print(
    interpret_expr(
        ast_generator.parse_expr(
            lexer.lex("2 + -(3 * 5) * 4 * 3 * 2")), {}
    )
)


print(
    interpret_phrase(
        ast_generator.parse_phrase(
            lexer.lex("~print(2, 3, 4);"))[0], {}
    )
)

print(ast_generator.parse_program(
    lexer.lex("~print(2, 3, 4); ~print(2, 3);"))
)

print(ast_generator.parse_program(
    lexer.lex("i := 0; ~print(3);")), {}
)
print(
    interpret_program(
        ast_generator.parse_program(
            lexer.lex("~print(2, 3, 4); i := 0; ~print(i);~i;")), {}
    )
)
