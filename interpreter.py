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
    if type(expr) == ast_generator.FloatValue:
        return expr.get_value()
    elif type(expr) == ast_generator.StrValue:
        return expr.get_value()
    elif type(expr) == ast_generator.BoolValue:
        return expr.get_value()
    elif type(expr) == ast_generator.Tuple:
        expr_list = expr.get_exprs()
        evaled_exprs = list(map(lambda e: interpret_expr(e, env), expr_list))
        return tuple(evaled_exprs)
    elif type(expr) == ast_generator.List:
        expr_list = expr.get_exprs()
        evaled_exprs = list(map(lambda e: interpret_expr(e, env), expr_list))
        return evaled_exprs
    elif type(expr) == ast_generator.Dict:
        key_list = expr.get_keys()
        val_list = expr.get_vals()
        evaled_keys = list(map(lambda e: interpret_expr(e, env), key_list))
        evaled_vals = list(map(lambda e: interpret_expr(e, env), val_list))
        combined_list = list(zip(evaled_keys, evaled_vals))
        new_dict = {pair[0]: pair[1] for pair in combined_list}
        return new_dict
    elif type(expr) == ast_generator.Struct:
        key_list = expr.get_keys()
        val_list = expr.get_vals()
        evaled_keys = list(map(lambda e: e.get_value(), key_list))
        evaled_vals = list(map(lambda e: interpret_expr(e, env), val_list))
        combined_list = list(zip(evaled_keys, evaled_vals))
        new_dict = {pair[0]: pair[1] for pair in combined_list}
        return new_dict
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
            return left / right
    elif type(expr) == ast_generator.Extern:
        return interpret_extern(expr, env)
    elif type(expr) == ast_generator.Apply:
        function_name = expr.get_fun()
        args_list = expr.get_args()
        args = list(map(lambda arg: interpret_expr(arg, env), args_list))

        function, defenv = env[("function", function_name)]
        function_body = function.get_body()
        function_params = function.get_args()
        params = list(map(lambda p: p.get_value(), function_params))

        if len(args) != len(function_params):
            raise InterpretError("Given args have different arity than function args: length of args is " +
                                 str(len(args)) + "!= length of params is " + str(len(function_params)))

        def assign_param(param, arg, env):
            env[("variable", param)] = arg

        func_env = deepcopy(defenv)
        _ = list(map(lambda arg, param: assign_param(
            param, arg, func_env), args, params))
        for phrase in function_body:
            try:
                func_env = interpret_phrase(phrase, func_env)
            except ReturnException as e:
                # return captured
                return e.get_ret_value()

        return 0  # return 0 if successful and no return


def interpret_extern(expr, env):
    function_name = expr.get_fun()
    args_list = expr.get_args()
    if function_name != ast_generator.SET_STRUCT and function_name != ast_generator.GET_STRUCT:
        args = list(map(lambda arg: interpret_expr(arg, env), args_list))
    else:
        args = args_list

    if function_name == ast_generator.PRINT:
        print(*args)
        return 1  # print extern returns 1 if it occurred
    elif function_name == ast_generator.MEM:
        if len(args_list) != 2:
            raise InterpretError(
                "Mem requires 2 arguments : You had: " + str(args_list))
        ob = args_list[0]
        ob = interpret_expr(ob, env)
        iterable = args_list[1]
        iterable = interpret_expr(iterable, env)
        return 1 if ob in iterable else 0
    elif function_name == ast_generator.LEN:
        if len(args_list) != 1:
            raise InterpretError(
                "Len requires 1 arguments : You had: " + str(args_list))
        lst = args_list[0]
        lst = interpret_expr(lst, env)
        return len(lst)
    elif function_name == ast_generator.GET:
        if len(args_list) != 2:
            raise InterpretError(
                "Get requires 2 arguments : You had: " + str(args_list))
        pos = args_list[0]
        pos = interpret_expr(pos, env)
        lst = args_list[1]
        lst = interpret_expr(lst, env)
        return lst[pos]
    elif function_name == ast_generator.GET_STRUCT:
        if len(args_list) != 2:
            raise InterpretError(
                "Get_Struct requires 2 arguments : You had: " + str(args_list))
        pos = args_list[0]
        assert type(pos) == ast_generator.VarValue
        pos = pos.get_value()  # must be a string
        lst = args_list[1]
        lst = interpret_expr(lst, env)
        return lst[pos]
    elif function_name == ast_generator.SET:
        if len(args_list) != 3:
            raise InterpretError(
                "Set requires 3 arguments : You had: " + str(args_list))
        pos = args_list[0]
        pos = interpret_expr(pos, env)
        new_val = args_list[1]
        new_val = interpret_expr(new_val, env)
        lst = args_list[2]
        lst = interpret_expr(lst, env)
        lst[pos] = new_val
        return 1  # set successfully
    elif function_name == ast_generator.SET_STRUCT:
        if len(args_list) != 3:
            raise InterpretError(
                "Set_Struct requires 3 arguments : You had: " + str(args_list))
        pos = args_list[0]
        assert type(pos) == ast_generator.VarValue
        pos = pos.get_value()  # must be a string
        new_val = args_list[1]
        new_val = interpret_expr(new_val, env)
        lst = args_list[2]
        lst = interpret_expr(lst, env)
        lst[pos] = new_val
        return 1  # set successfully

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

        new_env = deepcopy(env)
        while guard_value:  # using truthy values including non zero ints
            # one loop
            for sub_phrase in body_list:
                new_env = interpret_phrase(sub_phrase, new_env)  # update env
            # recalculate guard at bottom of loop to see if it continues
            guard_value = interpret_expr(guard_expr, new_env)
        return env
    elif type(phrase) == ast_generator.IfThenElse:
        (if_guard, if_body) = phrase.get_if_pair()
        (elif_guards, elif_bodies) = phrase.get_elif_pair_list()
        else_body = phrase.get_else()
        if_guard_value = interpret_expr(if_guard, env)
        if if_guard_value:
            new_env = deepcopy(env)
            for sub_phrase in if_body:
                new_env = interpret_phrase(sub_phrase, new_env)  # update env
            return env

        for i in range(len(elif_guards)):
            elif_guard = elif_guards[i]
            elif_guard_value = interpret_expr(elif_guard, env)
            if elif_guard_value:
                elif_body = elif_bodies[i]
                new_env = deepcopy(env)
                for sub_phrase in elif_body:
                    new_env = interpret_phrase(
                        sub_phrase, new_env)  # update env
                return env

        if else_body != None:
            new_env = deepcopy(env)
            for sub_phrase in else_body:
                new_env = interpret_phrase(
                    sub_phrase, new_env)  # update env
            return env

    elif type(phrase) == ast_generator.For:
        index = phrase.get_index()
        var_name = index.get_value()

        from_int = phrase.get_from()
        from_int = from_int.get_value()
        end_int = phrase.get_end()
        end_int = end_int.get_value()
        by = phrase.get_by()
        by = by.get_value()
        body_list = phrase.get_body()

        new_env = deepcopy(env)
        for idx in range(from_int, end_int + 1, by):
            new_env[("variable", var_name)] = idx
            for sub_phrase in body_list:
                new_env = interpret_phrase(sub_phrase, new_env)  # update env
        return env

    elif type(phrase) == ast_generator.Return:
        # leave current env and do not save it
        body_expr = phrase.get_body()
        value = interpret_expr(body_expr, env)
        raise ReturnException(value)
    elif type(phrase) == ast_generator.Ignore:
        expr = phrase.get_expr()
        _ = interpret_expr(expr, env)
        # do not bind as this is an ignore
        return env
    elif type(phrase) == ast_generator.Function:
        function_name = phrase.get_name()
        function_name = function_name.get_value()
        defenv = deepcopy(env)
        defenv[("function", function_name)] = (
            phrase, defenv)  # allowed in python but NOT OCAML, because RHS evaluates before LHS because RHS refers to variable value while LHS refers to variable memory location
        env[("function", function_name)] = (phrase, defenv)
        # closure at time of creation
        return env


def interpret_program(program, env):
    phrase_list = program.get_phrases()
    for phrase in phrase_list:
        env = interpret_phrase(phrase, env)
    return env


def interpret(program):
    assert type(program) == ast_generator.Program
    try:
        return interpret_program(program, {})
    except ReturnException as _:
        raise InterpretError(
            "You used a return statement when you were not in a function call")


def main(program):
    return interpret(ast_generator.parse_program(lexer.lex(program)))


if __name__ == "__main__":
    print(main("fun f x -> if x then x := x - 1; ~ print(x); return f(x); endif else return x; endelse endfun ~ f(10) ;"))

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

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("for i from 1 to 9 by 3 dofor ~print(i);endfor")), {}
        )
    )

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("i := 10; while i dowhile ~print(i); i := i - 1; endwhile")), {}
        )
    )

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("if 1 then ~print(1); endif")), {}
        )
    )

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("if 0 then ~print(1); endif else x := -22; ~print(x); endelse")), {}
        )
    )

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("if 0 then ~print(1); endif elif 1 then ~print(3); endelif else x := -22; ~print(x); endelse")), {}
        )
    )

    print(
        interpret_program(
            ast_generator.parse_program(
                lexer.lex("fun f x -> x := x + 1; ~print(x); endfun ~ f(3) ;")), {}
        )
    )

    print(main('x := "hello world!"; ~ print(x * 3);'))
    print(main('x := "hello world!"; y := (|(3 + 3)|);'))
    print(main('x := "hello world!"; t:= (|x, x|);~ print(t); ~print((|x, x|));'))
    print(main('x := "hello world!"; t:= (|x, x|);~ print(t); ~print((|x, (|x, x, x|), (x + x)|), x);'))

    print(main('x := "hello world!"; ~ print([x, x, x]);'))
    print(main(
        'x := "hello world!"; ~ print([x, x, x]); lst := [x, x]; ~ print(mem(x, lst));'))
    print(main(
        'x := "hello world!"; ~ print([x, x, x]); lst := [x, x]; ~ print(mem(x, lst)); ~print(len(lst));'))
    print(main(
        'x := "hello world!"; ~ print([x, x, x]); lst := [x, x]; ~ print(mem(x, lst)); ~print(len(lst)); ~print(get(0, lst));~print(get(1, lst));'))
    print(main(
        'x := "hello world!"; ~ print([x, x, x]); lst := [x, x]; ~ print(mem(x, lst)); ~print(len(lst)); ~set(0, "lol", lst);~print(get(0, lst)); ~print(lst);'))

    print(main('x := -1.00 - -2.01; ~print(x);'))

    print(main('x:={3 : 4}; ~print(get(3, x));'))

    print(main('x:={|x <- 4|}; '))
    print(main('x:={|x <- 4|}; ~print(get_struct(x, x));'))
    print(main('x:={|x <- 4|}; ~set_struct(x, "lol", x); ~print(x);'))
    print(main('x:={|x <- 4|}; ~set_struct(y, "lol", x); ~print(x);'))

    print(main('x:=True;'))
    print(main('x:=False;'))

    print(main('x:=-True;'))
    print(main('x:=-False;'))
