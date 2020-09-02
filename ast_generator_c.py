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

# ------- IMPORTS ------------


from copy import deepcopy
import lexer_c

# ------- CONSTANTS ------------


UNOP_PRECEDENCE = 4
START_PRECEDENCE = 1
N_PRECEDENCE_LEVELS = 4

PRECENDENCE_MAP = {
    lexer_c.PLUS: 1,
    lexer_c.MINUS: 1,
    lexer_c.TIMES: 2,
    lexer_c.DIV: 2,
    lexer_c.EXP: 3,
}


# ------- TYPE RELATED -------
WILDCARD_TYPE = "wildcard_type"  # matches empty list, empty dict key or value, etc


# ------- EXTERNS ------------
PRINT = "print"
MEM = "mem"
GET = "get"
GET_STRUCT = "get_struct"
LEN = "len"
SET = "set"
SET_STRUCT = "set_struct"
ADD_STRUCT = "add_struct"
DEL_STRUCT = "del_struct"
GET_ARR = "get_arr"
SET_ARR = "set_arr"
EXTERNS_LIST = [PRINT, MEM, GET, LEN, SET,
                GET_STRUCT, SET_STRUCT, ADD_STRUCT, DEL_STRUCT, GET_ARR, SET_ARR, ]

# ------- GRAMMAR PRODUCTION RULES ------------

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
#     lexer_c.PLUS,
#     lexer_c.MINUS,
#     lexer_c.TIMES,
#     lexer_c.DIV,
# ]

# EXPRESSION_RULES = [
#     [VALUE],
#     [EXPRESSION, BOP, EXPRESSION],
#     []

# ]


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


class AssignVariableException(Exception):
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


class Type(object):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(AbstractType: DO NOT INSTANTIATE!)"

    def __eq__(self, other):
        print("Two Abstract Types are never equal!")
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class IntType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(IntType)"

    def __eq__(self, other):
        return type(other) == IntType or type(other) == WildcardType

    def __ne__(self, other):
        return not self.__eq__(other)


class StrType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(StrType)"

    def __eq__(self, other):
        return type(other) == StrType or type(other) == WildcardType

    def __ne__(self, other):
        return not self.__eq__(other)


class FloatType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(FloatType)"

    def __eq__(self, other):
        return type(other) == FloatType or type(other) == WildcardType

    def __ne__(self, other):
        return not self.__eq__(other)


class BoolType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(BoolType)"

    def __eq__(self, other):
        return type(other) == BoolType or type(other) == WildcardType

    def __ne__(self, other):
        return not self.__eq__(other)


class WildcardType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "(WildcardType)"

    def __eq__(self, other):
        return isinstance(other, Type)

    def __ne__(self, other):
        return not self.__eq__(other)


class CustomType(Type):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return "(CustomType: " + str(self.name) + ")"

    def __eq__(self, other):
        # raise RuntimeError("NEVER TEST FOR CUSTOM TYPE EQUALITY!")
        if type(other) == WildcardType:
            return True
        if type(other) != CustomType:
            return False
        # may not be completely correct: other variants of the same type
        # are still false!
        return self.name == other.name

    def __ne__(self, other):
        # raise RuntimeError("NEVER TEST FOR CUSTOM TYPE INEQUALITY!")
        return not self.__eq__(other)


class UnionValue(Expr):
    def __init__(self, name, expr):
        super().__init__()
        self.name = name
        self.expr = expr

    def get_name(self):
        return self.name

    def get_expr(self):
        return self.expr

    def __repr__(self):
        return "(UnionValue: @" + str(self.name) + "(" + str(self.expr) + "))"


class DeclareUnion(Type):
    def __init__(self, name, typ_list):
        super().__init__()
        self.name = name
        self.typ_list = typ_list

    def get_name(self):
        return self.name

    def get_typ_list(self):
        return self.typ_list

    def __repr__(self):
        return "(UnionDeclaration: " + str(self.name) + " " + str(self.typ_list) + ")"

    def __eq__(self, other):
        if type(other) == WildcardType:
            return True
        if type(other) != DeclareUnion:
            return False
        self_name = self.get_name()
        other_name = other.get_name()
        if self_name != other_name:
            return False
        self_typ_list = self.get_typ_list()
        other_typ_list = other.get_typ_list()
        if len(self_typ_list) != len(other_typ_list):
            return False
        # order of declarations does not matter, as long as they are
        # they exist in both Union Types
        for typ in self_typ_list:
            has_match = False
            for other_typ in self_typ_list:
                if typ == other_typ:
                    has_match = True
            if not has_match:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class DeclareStruct(Type):
    def __init__(self, name, typ_list):
        super().__init__()
        self.name = name
        self.typ_list = typ_list

    def get_name(self):
        return self.name

    def get_typ_list(self):
        return self.typ_list

    def __repr__(self):
        return "(StructDeclaration: " + str(self.name) + " " + str(self.typ_list) + ")"

    def __eq__(self, other):
        if type(other) == WildcardType:
            return True
        if type(other) != DeclareStruct:
            return False
        self_name = self.get_name()
        other_name = other.get_name()
        if self_name != other_name:
            return False
        self_typ_list = self.get_typ_list()
        other_typ_list = other.get_typ_list()
        if len(self_typ_list) != len(other_typ_list):
            return False
        # order of declarations does not matter, as long as they are
        # they exist in both Struct Types
        for typ in self_typ_list:
            has_match = False
            for other_typ in self_typ_list:
                if typ == other_typ:
                    has_match = True
            if not has_match:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class TupleType(Type):
    def __init__(self, typ_list):
        super().__init__()
        self.typ_list = typ_list

    def get_typ(self):
        return self.typ_list

    def __repr__(self):
        return "(TupleType: " + str(self.typ_list) + ")"

    def __eq__(self, other):
        if type(other) == WILDCARD_TYPE:
            return True
        if type(other) != TupleType:
            return False
        other_typ_list = other.get_typ()
        self_typ_list = self.get_typ()
        if len(other_typ_list) != len(self_typ_list):
            return False
        for i in range(len(self_typ_list)):
            self_item = self_typ_list[i]
            other_item = other_typ_list[i]
            if self_item != other_item:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class ListType(Type):
    def __init__(self, typ):
        super().__init__()
        self.typ = typ

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(ListType: " + str(self.typ) + ")"

    def __eq__(self, other):
        return (type(other) == ListType and other.get_typ() == self.get_typ()) or \
            (type(other) == WildcardType)

    def __ne__(self, other):
        return not self.__eq__(other)


class ArrayType(Type):
    def __init__(self, typ, length):
        super().__init__()
        assert type(length) == int
        self.typ = typ
        self.length = length

    def get_typ(self):
        return self.typ

    def get_len(self):
        return self.length

    def __repr__(self):
        return "(ArrayType: " + str(self.typ) + "<" + str(self.length) + ">" + ")"

    def __eq__(self, other):
        return (type(other) == ArrayType and other.get_typ() == self.get_typ()) or \
            (type(other) == WildcardType)

    def __ne__(self, other):
        return not self.__eq__(other)


class DictType(Type):
    def __init__(self, key_typ, val_typ):
        super().__init__()
        self.key_typ = key_typ
        self.val_typ = val_typ

    def get_key_typ(self):
        return self.key_typ

    def get_val_typ(self):
        return self.val_typ

    def __repr__(self):
        return "(DictType: " + str(self.key_typ) + " : " + str(self.val_typ) + ")"

    def __eq__(self, other):
        return (type(other) == DictType and other.get_key_typ() == self.get_key_typ() and other.get_val_typ() == self.get_val_typ()) or \
            (type(other) == WildcardType)

    def __ne__(self, other):
        return not self.__eq__(other)


class FuncType(Type):
    def __init__(self, ret_typ, args_typs_lst):
        super().__init__()
        self.ret_typ = ret_typ
        self.args_typs = args_typs_lst

    def get_ret_typ(self):
        return self.ret_typ

    def get_args_typs(self):
        return self.args_typs

    def __repr__(self):
        typs = deepcopy(self.args_typs)
        typs.append(self.ret_typ)
        return "(FunctionType: " + (str(lexer_c.FUN_ARROW)).join(list(map(lambda t: str(t), typs))) + ")"

    def __eq__(self, other):
        if type(other) == WILDCARD_TYPE:
            return True
        if type(other) != FuncType:
            return False
        if self.get_ret_typ() != other.get_ret_typ():
            return False
        other_typ_list = other.get_args_typs()
        self_typ_list = self.get_args_typs()
        if len(other_typ_list) != len(self_typ_list):
            return False
        for i in range(len(self_typ_list)):
            self_item = self_typ_list[i]
            other_item = other_typ_list[i]
            if self_item != other_item:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


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


class BoolValue(Expr):
    """
    BoolValue represents an Bool Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(BoolValue: " + str(self.value) + ")"


class FloatValue(Expr):
    """
    FloatValue represents an float Value
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(FloatValue: " + str(self.value) + ")"


class StrValue(Expr):
    """
    StrValue represents an String
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "(StrValue: " + str(self.value) + ")"


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


class Tuple(Expr):
    """
    Tuple represents an Tuple
    """

    def __init__(self, exprs_list):
        super().__init__()
        self.exprs = exprs_list
        self.length = len(exprs_list)

    def get_exprs(self):
        return self.exprs

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Tuple: (" + ", ".join(list(map(lambda e: str(e), self.exprs))) + "))"


class Array(Expr):
    """
    Array represents an array
    """

    def __init__(self, exprs_list):
        super().__init__()
        self.exprs = exprs_list
        self.length = len(exprs_list)

    def get_exprs(self):
        return self.exprs

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Array: (" + ", ".join(list(map(lambda e: str(e), self.exprs))) + "))"


class List(Expr):
    """
    List represents an list
    """

    def __init__(self, exprs_list):
        super().__init__()
        self.exprs = exprs_list
        self.length = len(exprs_list)

    def get_exprs(self):
        return self.exprs

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(List: [" + ", ".join(list(map(lambda e: str(e), self.exprs))) + "])"


class Dict(Expr):
    """
    Dict represents an dictionary
    """

    def __init__(self, keys_list, values_list):
        super().__init__()
        assert len(keys_list) == len(values_list)
        self.keys = keys_list
        self.values = values_list
        self.length = len(values_list)

    def get_keys(self):
        return self.keys

    def get_vals(self):
        return self.values

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Dict: {" + ", ".join(list(map(lambda k, v: str(k) + " : " + str(v), self.keys, self.values))) + "})"


class Struct(Expr):
    """
    Struct represents an struct
    """

    def __init__(self, keys_list, values_list):
        super().__init__()
        assert len(keys_list) == len(values_list)
        joined_list = list(zip(keys_list, values_list))
        joined_list = sorted(
            joined_list, key=lambda pair: pair[0].get_value())  # sort by key
        keys_list, values_list = list(zip(*joined_list))
        self.keys = keys_list
        self.values = values_list
        self.length = len(values_list)

    def get_keys(self):
        return self.keys

    def get_vals(self):
        return self.values

    def get_length(self):
        return self.length

    def __repr__(self):
        return "(Struct: {|" + ", ".join(list(map(lambda k, v: str(k) + " : " + str(v), self.keys, self.values))) + "|})"


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


class Declaration(Expr):
    """
    declaration represents type var assign expre
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def set_assign(self, assign):
        self.assign = assign

    def set_typ(self, typ):
        self.typ = typ

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(Declaration: " + str(self.typ) + " " + str(self.assign) + ")"


class DeclareTuple(Expr):
    """
    DeclareTupleTuple represents an type declaration var := tuple
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(DeclareTuple: " + str(self.typ) + " " + str(self.assign) + ")"


class DeclareList(Expr):
    """
    DeclareList represents an type declaration var := list
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(DeclareList: " + str(self.typ) + " " + str(self.assign) + ")"


class DeclareArray(Expr):
    """
    DeclareArray represents an type declaration var := arry
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(DeclareArray: " + str(self.typ) + " " + str(self.assign) + ")"


class DeclareDict(Expr):
    """
    DeclareDict represents an {t1 : t2} }var := dictimonary
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(DeclareDict: " + str(self.typ) + " " + str(self.assign) + ")"


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

    def get_index(self):
        return self.index

    def get_from(self):
        return self.from_int

    def get_end(self):
        return self.end_int

    def get_by(self):
        return self.by

    def get_body(self):
        return self.body

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

    def get_name(self):
        return self.name

    def get_args(self):
        return self.args

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(fun " + str(self.name) + " " + " ".join(list(map(lambda arg: str(arg), self.args))) + " ->\n\t" + "\n\t".join(list(map(lambda phrase: str(phrase), self.body))) + "\nendfun)"


class DeclareFunc(Expr):
    """
    DeclareFunc represents an fun (|t1 -> t2|) name -> body endfun
    """

    def __init__(self, typ, assign):
        super().__init__()
        self.typ = typ
        self.assign = assign

    def get_assign(self):
        return self.assign

    def get_typ(self):
        return self.typ

    def __repr__(self):
        return "(DeclareFunc: " + str(self.typ) + " " + str(self.assign) + ")"


class IfThenElse(Expr):
    """
    IFThenElse represents an if then else erpression
    """

    def __init__(self, if_guard, if_body, elif_guards=[], elif_bodies=[], else_body=None):
        super().__init__()
        self.if_pair = (if_guard, if_body)
        self.elif_list = (elif_guards, elif_bodies)
        self.else_body = else_body

    def get_if_pair(self):
        return self.if_pair

    def get_elif_pair_list(self):
        return self.elif_list

    def get_else(self):
        return self.else_body

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


class Extern(Expr):
    """
    Extern represents fun extern (arg1 arg2...) with possibly no args as in
    extern () , with only open and close brackets.
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
        return "(Extern: " + str(self.fun) + "(" + (" ".join(list(map(lambda a: str(a), self.args_list)))) + ")" + ")"


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

    def get_body(self):
        return self.body

    def __repr__(self):
        return "(Return: " + str(self.body) + ";)"


class Ignore(Expr):
    """
    ignore represents
    expr;
    """

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def get_expr(self):
        return self.expr

    def __repr__(self):
        return "(Ignore: " + str(self.expr) + ";)"


class Program(Expr):
    """
    Program represents a syntacucally valid program
    """

    def __init__(self, phrase_list=[]):
        super().__init__()
        self.phrases = phrase_list

    def get_phrases(self):
        return self.phrases

    def __repr__(self):
        return "(Program:\n" + "\n".join(list(map(lambda phrase: str(phrase), self.phrases))) + "\n)"


# ------ MATCH FUNCTIONS --------

# def match_integer(lexbuf, val):
#     return match_expr(IntValue(val), lexbuf)


def get_between_brackets(lex_buff, idx, start=lexer_c.LPAREN, end=lexer_c.RPAREN):
    # assume start after idx
    stack = []
    stack.append(start)
    expr_terms = []
    i = idx

    while (i < len(lex_buff) and stack != []):

        typ, val = lex_buff[i]
        if val == start:
            stack.append(val)
        elif val == end:
            if stack != [] and stack[-1] == start:
                stack.pop()
        expr_terms.append((typ, val))
        i += 1

    if i > len(lex_buff):
        raise MissingParens("Missing or Misplaced Parentheses")
    if stack != []:
        raise MissingParens("Missing or Misplaced Parentheses")
    l = len(expr_terms)
    expr_terms.pop()  # removd last parentheses
    return (l, expr_terms)


def get_between_brackets_general(lex_buff, idx, start_sym, end_sym):
    # assume start after idx
    stack = []
    stack.append(start_sym)
    expr_terms = []
    i = idx

    while (i < len(lex_buff) and stack != []):

        typ, val = lex_buff[i]
        # if val == start_sym:
        #     stack.append(val)
        # elif val == end_sym:
        #     if stack != [] and stack[-1] == start_sym:
        #         stack.pop()
        if val == lexer_c.LPAREN:
            stack.append(val)
        elif val == lexer_c.RPAREN:
            if stack != [] and stack[-1] == lexer_c.LPAREN:
                stack.pop()

        if val == lexer_c.OPEN_TUP:
            stack.append(val)
        elif val == lexer_c.CLOSE_TUP:
            if stack != [] and stack[-1] == lexer_c.OPEN_TUP:
                stack.pop()

        if val == lexer_c.OPEN_BRACKET:
            stack.append(val)
        elif val == lexer_c.CLOSE_BRACKET:
            if stack != [] and stack[-1] == lexer_c.OPEN_BRACKET:
                stack.pop()

        if val == lexer_c.OPEN_DICT:
            stack.append(val)
        elif val == lexer_c.CLOSE_DICT:
            if stack != [] and stack[-1] == lexer_c.OPEN_DICT:
                stack.pop()

        if val == lexer_c.OPEN_STRUCT:
            stack.append(val)
        elif val == lexer_c.CLOSE_STRUCT:
            if stack != [] and stack[-1] == lexer_c.OPEN_STRUCT:
                stack.pop()

        if val == lexer_c.OPEN_ARRAY:
            stack.append(val)
        elif val == lexer_c.CLOSE_ARRAY:
            if stack != [] and stack[-1] == lexer_c.OPEN_ARRAY:
                stack.pop()

        expr_terms.append((typ, val))
        i += 1

    if i > len(lex_buff):
        raise MissingParens("Missing or Misplaced End Symbol")
    if stack != []:
        raise MissingParens("Missing or Misplaced End Symbol")
    l = len(expr_terms)
    expr_terms.pop()  # removed last parentheses
    return (l, expr_terms)


# def match_open_paren(ast, lex_buff):

#     lex_typ, val = lex_buff[0]
#     if val != lexer_c.LPAREN:
#         return None

#     middle_terms, length = get_between_brackets(lex_buff[1:], 0)
#     new_lex_buff = lex_buff[1 + length:]
#     new_ast = match_expr(None, middle_terms)

#     if ast != None:
#         ast.set_right(new_ast)

#     else:
#         ast = new_ast

#     return match_expr(ast, new_lex_buff)


# def match_bop(ast, lexbuf, bop):
#     bop_node = Bop(bop)
#     bop_node.set_left(ast)
#     # need to wrap in try.except if theis is undefined
#     head = lexbuf[0]
#     la_typ, la_val = head
#     if (bop == lexer_c.TIMES or bop == lexer_c.DIV) and la_typ in lexer_c.INTEGER:
#         right_node = match_expr(None, [head])
#         bop_node.set_right(right_node)
#         tail = lexbuf[1:]
#         return match_expr(bop_node, tail)
#     elif (bop == lexer_c.TIMES or bop == lexer_c.DIV) and la_val == lexer_c.LPAREN:
#         right_node = match_open_paren(bop_node, lexbuf)
#         return right_node
#     else:
#         right_node = match_expr(None, lexbuf)
#         bop_node.set_right(right_node)

#     return bop_node


# def match_unop(lexbuf, unop):
#     unop_node = Unop(unop)
#     head = lexbuf[0]
#     tail = lexbuf[1:]
#     la_typ, _ = head
#     if la_typ in lexer_c.INTEGER:
#         bottom_node = match_expr(None, [head])
#         unop_node.set_expr(bottom_node)
#         return match_expr(unop_node, tail)
#     raise UnopAdditionalArg(
#         "Additional arg to a unary operation %s" % (unop))


# def match_expr(ast, lexbuf):
#     """
#     match_expr(ast, lexbuf) creates an ast from lexbuf, otherwise raises
#     appropriate execption
#     """
#     if lexbuf == []:
#         return ast

#     typ, val = lexbuf[0]
#     tail = lexbuf[1:]

#     if typ == lexer_c.INTEGER:
#         return match_integer(tail, val)
#     elif ast == None and val in lexer_c.UNOPS:
#         return match_unop(tail, val)
#     elif ast == None and val in lexer_c.BOPS:
#         raise BopMissingArg("Missing arg %s" % (val))
#     elif ast != None and val in lexer_c.BOPS:
#         return match_bop(ast, tail, val)
#     elif ast != None and val in lexer_c.UNOPS:
#         raise UnopAdditionalArg(
#             "Additional arg to a unary operation %s" % (val))
#     elif val == lexer_c.LPAREN:
#         return match_open_paren(ast, lexbuf)
#         # return match_lparent(ast, tail, val)
#     elif val == lexer_c.RPAREN:
#         raise UnmatchedParenError("Unmatched right parenthesis %s" % (val))

#     raise ParseError("Error in Parsing Tokens")


# def match(lexbuf):
#     """
#     match(lexbuf) creates an ast from from lexbuf, otherwises
#     raises an appropriate exeception
#     """
#     ast = None
#     return match_expr(ast, lexbuf)


# def parse(lex_buff):
#     def parse_helper(lex_buff, ast, stack):
#         if lex_buff == []:
#             return
#     return parse_helper(lex_buff, AST(), [])


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
        new_stack = deepcopy(stack[3:])
        new_stack.insert(0, Bop(bop, start, end))
        return reduce_stack(precedence, new_stack)

    elif precedence == 4:
        unop = stack[0][1]
        val = stack[1]
        new_stack = deepcopy(stack[2:])
        new_stack.insert(0, Unop(unop, val))
        return reduce_stack(precedence, new_stack)


def get_function_args(lexbuf, demarcation):
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

        if val == lexer_c.LPAREN:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.RPAREN:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.LPAREN:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens("lexbuf missing left parens")

        if val == lexer_c.OPEN_TUP:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.CLOSE_TUP:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.OPEN_TUP:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens("lexbuf missing open tup parens")

        if val == lexer_c.OPEN_BRACKET:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.CLOSE_BRACKET:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.OPEN_BRACKET:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens("lexbuf missing open bracket")

        if val == lexer_c.OPEN_DICT:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.CLOSE_DICT:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.OPEN_DICT:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens(
                    "lexbuf missing open dictionary symbol : {")

        if val == lexer_c.OPEN_STRUCT:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.CLOSE_STRUCT:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.OPEN_STRUCT:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens(
                    "lexbuf missing open dictionary symbol : {|")

        if val == lexer_c.OPEN_ARRAY:
            stack.append(val)
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

        elif val == lexer_c.CLOSE_ARRAY:
            if len(stack) >= 1:
                if stack[-1] == lexer_c.OPEN_ARRAY:
                    stack.pop()
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
                else:
                    stack.append(val)
                    arg.append(pair)
                    return get_function_args_helper(rem, demarcation, stack, arg, args_list)
            else:
                raise MissingParens(
                    "lexbuf missing open array symbol : [|")

        else:
            arg.append(pair)
            return get_function_args_helper(rem, demarcation, stack, arg, args_list)

    return get_function_args_helper(lexbuf, demarcation, [], [], [])


# def get_data_structure_args(lexbuf, demarcation, start_char, end_char):
#     def get_data_structure_args_helper(lexbuf, demarcation, stack, arg, args_list):
#         if lexbuf == []:
#             if arg != []:
#                 args_list.append(arg)
#             return args_list

#         pair = lexbuf[0]
#         _, val = pair
#         rem = lexbuf[1:]

#         if stack == [] and val == demarcation:
#             args_list.append(arg)
#             return get_data_structure_args_helper(rem, demarcation, stack, [], args_list)

#         if val == lexer_c.LPAREN:
#             stack.append(val)
#             arg.append(pair)
#             return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)

#         elif val == lexer_c.RPAREN:
#             if len(stack) >= 1:
#                 if stack[-1] == lexer_c.LPAREN:
#                     stack.pop()
#                     arg.append(pair)
#                     return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)
#                 else:
#                     stack.append(val)
#                     arg.append(pair)
#                     return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)
#             else:
#                 raise MissingParens("lexbuf missing left parens")

#         if val == start_char:
#             stack.append(val)
#             arg.append(pair)
#             return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)

#         elif val == end_char:
#             if len(stack) >= 1:
#                 if stack[-1] == start_char:
#                     stack.pop()
#                     arg.append(pair)
#                     return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)
#                 else:
#                     stack.append(val)
#                     arg.append(pair)
#                     return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)
#             else:
#                 raise MissingParens("lexbuf missing end char " + str(end_char))

#         else:
#             arg.append(pair)
#             return get_data_structure_args_helper(rem, demarcation, stack, arg, args_list)

#     return get_data_structure_args_helper(lexbuf, demarcation, [], [], [])


# def parse_expr(prev_precedence, count, precedence, stack, lexbuf):

#     # ----------- 0 tokens remaining = nothing more to parse ----------
#     # ----------- Used to escape if start call has 0 tokens  ----------
#     if lexbuf == []:
#         return (count, reduce_stack(precedence, stack))

#     typ_curr, val_curr = lexbuf[0]

#     # --------- One Token REMANING ------------
#     if len(lexbuf) <= 1:
#         new_stack = deepcopy(stack)
#         if typ_curr == lexer_c.INTEGER:
#             new_stack.append(IntValue(val_curr))
#         elif typ_curr == lexer_c.VARIABLE:
#             new_stack.append(VarValue(val_curr))
#         else:
#             raise EndWithOperatorError(val_curr)
#         return (count + 1, reduce_stack(precedence, new_stack))

#     # --------- TWO OR MORE Tokens REMANING ------------
#     type_la, val_la = lexbuf[1]

#     # --------- INT AND LOOKAHEAD ------------
#     if typ_curr == lexer_c.INTEGER:
#         if type_la == lexer_c.INTEGER or type_la == lexer_c.VARIABLE:
#             raise ParseError(
#                 "Integer cannot be followed by a variable or integer")

#         new_precedence = get_precedence(val_la, PRECENDENCE_MAP)

#         if new_precedence > precedence:
#             new_stack = []
#             new_stack.append(IntValue(val_curr))
#             new_idx, res_ast = parse_expr(precedence,
#                                           0, new_precedence, new_stack, lexbuf[1:])
#             stack.append(res_ast)
#             return parse_expr(prev_precedence, count + new_idx + 1, precedence, stack, lexbuf[1 + new_idx:])

#         elif new_precedence == precedence:
#             stack.append(IntValue(val_curr))
#             # reduced_stack = reduce_stack(precedence, stack)
#             return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[1:])

#         else:

#             stack.append(IntValue(val_curr))
#             res_ast = reduce_stack(precedence, stack)

#             # ------- when invariant is correct, not needed ---------
#             # next_precedence = get_precedence(
#             #     lexbuf[1][1], PRECENDENCE_MAP) if len(lexbuf) >= 2 else -1
#             # if prev_precedence < next_precedence:
#             #     next_stack = []
#             #     next_stack.append(res_ast)

#             #     return parse_expr(precedence, count + 1, next_precedence, next_stack, lexbuf[1:])
#             # ------- when invariant is correct, not needed ---------

#             return count + 1, res_ast

#     # parse variables
#     elif typ_curr == lexer_c.VARIABLE:

#         if type_la == lexer_c.INTEGER or type_la == lexer_c.VARIABLE:
#             raise ParseError(
#                 "Variable cannot be followed by a variable or integer")
#         elif val_la == lexer_c.RPAREN:
#             raise UnmatchedParenError(
#                 "Unmatched right parenthesis %s" % (val_curr))

#         # parse function
#         elif val_la == lexer_c.LPAREN:

#             middle_terms, length = get_between_brackets(lexbuf[2:], 0)
#             split_args = get_function_args(middle_terms, lexer_c.COMMA)

#             args_pairs = list(map(lambda args_buffer: parse_expr(
#                 1, 0, 1, [], args_buffer), split_args))
#             args = list(map(lambda pair: pair[1], args_pairs))
#             apply_obj = Apply(val_curr, args)

#             # do the lookahead
#             if len(lexbuf) > length + 2:
#                 _, val_la2 = lexbuf[(length + 2)]
#                 new_precedence_2 = get_precedence(val_la2, PRECENDENCE_MAP)
#                 if new_precedence_2 > precedence:

#                     new_stack = []
#                     new_stack.append(apply_obj)
#                     new_idx, res_ast = parse_expr(precedence,
#                                                   0, new_precedence_2, new_stack, lexbuf[(length + 2):])
#                     stack.append(res_ast)
#                     return parse_expr(prev_precedence, count + new_idx + length + 2, precedence, stack, lexbuf[2 + length + new_idx:])

#                 elif new_precedence_2 == precedence:
#                     stack.append(apply_obj)
#                     # reduced_stack = reduce_stack(precedence, stack)
#                     return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[(length + 2):])

#                 else:
#                     stack.append(apply_obj)
#                     res_ast = reduce_stack(precedence, stack)

#                     # ------- when invariant is correct, not needed ---------
#                     # next_precedence = get_precedence(
#                     #     lexbuf[(length + 2)][1], PRECENDENCE_MAP) if len(lexbuf) >= 2 else -1

#                     # if prev_precedence < next_precedence:

#                     #     next_stack = []
#                     #     next_stack.append(res_ast)
#                     #     return parse_expr(precedence, count + 1, next_precedence, next_stack, lexbuf[(length + 2):])
#                     # ------- when invariant is correct, not needed ---------

#                     return count + length + 2, res_ast

#             stack.append(apply_obj)
#             return parse_expr(prev_precedence, count + length + 2, precedence, stack, lexbuf[2 + length:])

#         # just a variable
#         else:
#             new_precedence = get_precedence(val_la, PRECENDENCE_MAP)

#             if new_precedence > precedence:
#                 new_stack = []
#                 new_stack.append(VarValue(val_curr))
#                 new_idx, res_ast = parse_expr(precedence,
#                                               0, new_precedence, new_stack, lexbuf[1:])
#                 stack.append(res_ast)
#                 return parse_expr(prev_precedence, count + new_idx + 1, precedence, stack, lexbuf[1 + new_idx:])

#             elif new_precedence == precedence:
#                 stack.append(VarValue(val_curr))
#                 # reduced_stack = reduce_stack(precedence, stack)
#                 return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[1:])

#             else:
#                 stack.append(IntValue(val_curr))
#                 res_ast = reduce_stack(precedence, stack)

#                 # ------- when invariant is correct, not needed ---------
#                 # next_precedence = get_precedence(
#                 #     lexbuf[1][1], PRECENDENCE_MAP) if len(lexbuf) >= 2 else -1
#                 # if prev_precedence < next_precedence:
#                 #     next_stack = []
#                 #     next_stack.append(res_ast)
#                 #     return parse_expr(precedence, count + 1, next_precedence, next_stack, lexbuf[1:])
#                 # ------- when invariant is correct, not needed ---------

#                 return count + 1, res_ast

#     elif val_curr == lexer_c.LPAREN:
#         middle_terms, length = get_between_brackets(lexbuf[1:], 0)
#         _, parens_ast = parse_expr(1, 0, 1, [], middle_terms)

#         # need to do a lookahead
#         if len(lexbuf) > 1 + length:
#             _, val_la2 = lexbuf[(length + 1)]
#             new_precedence_2 = get_precedence(val_la2, PRECENDENCE_MAP)
#             if new_precedence_2 > precedence:

#                 new_stack = []
#                 new_stack.append(parens_ast)
#                 new_idx, res_ast = parse_expr(precedence,
#                                               0, new_precedence_2, new_stack, lexbuf[(length + 1):])
#                 stack.append(res_ast)
#                 return parse_expr(prev_precedence, count + new_idx + length + 1, precedence, stack, lexbuf[1 + length + new_idx:])

#             elif new_precedence_2 == precedence:
#                 stack.append(parens_ast)
#                 # reduced_stack = reduce_stack(precedence, stack)
#                 return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[(length + 1):])

#             else:
#                 stack.append(parens_ast)
#                 res_ast = reduce_stack(precedence, stack)

#                 # ------- when invariant is correct, not needed ---------
#                 # next_precedence = get_precedence(
#                 #     lexbuf[(length + 1)][1], PRECENDENCE_MAP) if len(lexbuf) >= 2 else -1

#                 # if prev_precedence < next_precedence:

#                 #     next_stack = []
#                 #     next_stack.append(res_ast)
#                 #     return parse_expr(precedence, count + 1, next_precedence, next_stack, lexbuf[(length + 1):])
#                 # ------- when invariant is correct, not needed ---------

#                 return count + length + 1, res_ast

#         stack.append(parens_ast)
#         return parse_expr(prev_precedence, count + length + 1, precedence, stack, lexbuf[1 + length:])

#     elif val_curr == lexer_c.RPAREN:
#         raise UnmatchedParenError(
#             "Unmatched right parenthesis %s" % (val_curr))

#     elif val_curr in lexer_c.OPERATIONS:

#         if stack == []:
#             # unop case (Negation)
#             new_stack = []
#             new_stack.append(lexbuf[0])
#             unop_precedence = 4
#             shift, res_ast = parse_expr(
#                 precedence, 0, unop_precedence, new_stack, lexbuf[1:])
#             stack.append(res_ast)

#             return parse_expr(prev_precedence, count + shift + 1, precedence, stack, lexbuf[1 + shift:])
#         elif val_la in lexer_c.UNOPS:
#             # unop case (Negation)
#             new_stack = []
#             stack.append(lexbuf[0])
#             new_stack.append(lexbuf[1])
#             unop_precedence = 4
#             shift, res_ast = parse_expr(
#                 precedence, 1, unop_precedence, new_stack, lexbuf[2:])
#             stack.append(res_ast)

#             return parse_expr(prev_precedence, count + shift + 1, precedence, stack, lexbuf[1 + shift:])

#         stack.append(lexbuf[0])

#         # ------- when invariant is correct, not needed ---------
#         if precedence != get_precedence(val_curr, PRECENDENCE_MAP):
#             # issue here
#             shift, ast = parse_expr(
#                 precedence, 0, get_precedence(val_curr, PRECENDENCE_MAP), [], lexbuf[1:])
#             stack.append(ast)
#             return parse_expr(prev_precedence, count + shift + 1, precedence, stack, lexbuf[1 + shift:])
#         # ------- when invariant is correct, not needed ---------

#         return parse_expr(prev_precedence, count + 1, precedence, stack, lexbuf[1:])

#     else:
#         raise ParseError("Unknown Symbol")


def parse_func_type(lexbuf, sep=lexer_c.FUN_ARROW):
    """
    parse_func_type(lexbuf, sep) parses a stream that begins with an open TUP parentheses
    symbol (| (lexer_c.OPEN_TUP), which is delineted by symbol sep
    token sare the symbols in lexbuf
    the 0th symbol in lexbuf must be a open parentheses (

    SEP is typically a FUN_ARROW or ->
    """
    component_types = []
    for component_section in get_function_args(lexbuf, sep):
        if component_section == []:
            raise ParseError(
                "Two -> cannot follow each other, nor can a -> be at the beginning or end.")
        component_type = parse_type(component_section)
        component_types.append(component_type)
    if len(component_types) != 2:
        raise ParseError(
            "Functions Must Have At Least One Argument and One Return Type.")
    l = len(component_types)
    return FuncType(component_types[l - 1], component_types[:l - 1])


def parse_dict_type(lexbuf, sep=lexer_c.COLON):
    """
    parse_dict_type(lexbuf, sep) parses a stream that begins with an open brace parentheses
    symbol { (lexer_c.OPEN_DICT), which is delineted by symbol sep
    token sare the symbols in lexbuf
    the 0th symbol in lexbuf must be a open parentheses

    SEP is typically a COLON or :
    """
    component_types = []
    for component_section in get_function_args(lexbuf, sep):
        if component_section == []:
            raise ParseError(
                "Two : cannot follow each other, nor can a : be at the beginning or end.")
        component_type = parse_type(component_section)
        component_types.append(component_type)
    if len(component_types) != 2:
        raise ParseError(
            "Dictionaries Must Have Exactly 2 types.")
    return DictType(component_types[0], component_types[1])


def parse_tuple_type(lexbuf, sep=lexer_c.TIMES):
    """
    parse_tuple_type(lexbuf) parses a stream that begins with an open parentheses
    symbol, which is delineted by symbol sep
    token sare the symbols in lexbuf
    the 0th symbol in lexbuf must be a open parentheses

    SEP is typically a TIMES or *
    """
    component_types = []
    for component_section in get_function_args(lexbuf, sep):
        if component_section == []:
            raise ParseError(
                "Two * cannot follow each other, nor can a * be at the beginning or end.")
        component_type = parse_type(component_section)
        component_types.append(component_type)
    if len(component_types) < 2:
        raise ParseError(
            "Tuples must have 2 or more types for each of the corresponding components.")
    return TupleType(component_types)


def parse_list_type(lexbuf):
    """
    parse_list_type(lexbuf, tokens) parses the lexbuf into a lis ttype
    """
    return ListType(parse_type(lexbuf))


def parse_array_type(lexbuf):
    """
    parse_array_type(lexbuf) parses the lexbuf into a array ttype
    """
    assert lexbuf[-1][1] == lexer_c.GT
    assert lexbuf[-3][1] == lexer_c.LT
    assert lexbuf[-2][0] == lexer_c.INTEGER

    arr_length = lexbuf[-2][1]
    assert arr_length >= 0

    arr_type = parse_type(lexbuf[:-3])
    return ArrayType(arr_type, arr_length)


def parse_type(lexbuf):
    """
    Given a lexbuf that DEFINITEVLY contains a type, parses the tyupe out
    and returns the correct type
    """
    if lexbuf == []:
        raise ParseError(
            f"Cannot be empty type when parsing lexbuf stream: {lexbuf}.")
    elif len(lexbuf) == 1 and lexbuf[0][1] in lexer_c.TYPES:
        typ = lexbuf[0][1]
        return base_type_to_type_obj(typ)
    elif len(lexbuf) == 1 and lexbuf[0][0] == lexer_c.VARIABLE:
        typ = lexbuf[0][1]
        return CustomType(typ)
    elif lexbuf[0][1] == lexer_c.OPEN_BRACKET:
        l, _ = get_between_brackets(
            lexbuf, 1, start=lexer_c.OPEN_BRACKET, end=lexer_c.CLOSE_BRACKET)  # start 1 aheaf
        inner_lexbuf = lexbuf[1: l]
        inner_lst_typ = parse_list_type(
            inner_lexbuf)
        return inner_lst_typ
    elif lexbuf[0][1] == lexer_c.LPAREN:
        l, _ = get_between_brackets(lexbuf, 1)  # start 1 aheaf
        tup_type = parse_tuple_type(
            lexbuf[1:l], lexer_c.TIMES)
        return tup_type
    elif lexbuf[0][1] == lexer_c.OPEN_DICT:
        l, _ = get_between_brackets(
            lexbuf, 1, lexer_c.OPEN_DICT, lexer_c.CLOSE_DICT)  # start 1 aheaf
        dict_type = parse_dict_type(
            lexbuf[1:l], lexer_c.COLON)
        return dict_type
    elif lexbuf[0][1] == lexer_c.OPEN_TUP:
        l, _ = get_between_brackets(
            lexbuf, 1, lexer_c.OPEN_TUP, lexer_c.CLOSE_TUP)  # start 1 ahead
        func_type = parse_func_type(
            lexbuf[1:l], lexer_c.FUN_ARROW)
        return func_type
    elif lexbuf[0][1] == lexer_c.OPEN_ARRAY:
        l, _ = get_between_brackets(
            lexbuf, 1, start=lexer_c.OPEN_ARRAY, end=lexer_c.CLOSE_ARRAY)  # start 1 aheaf
        inner_lexbuf = lexbuf[1: l]
        inner_arr_typ = parse_array_type(
            inner_lexbuf)
        return inner_arr_typ
    raise ParseError(
        f"Malformed type definition when parsing lexbuf stream: {lexbuf}.")


def base_type_to_type_obj(typ):
    """
    base_type_to_type_obj(typ) converts a base typ like 'int' to IntType()
    or 'str' to StrType or 'float' to FloatType or 'bool' to BoolType.
    """
    if typ == lexer_c.INT:
        return IntType()
    elif typ == lexer_c.BOOL:
        return BoolType()
    elif typ == lexer_c.STR:
        return StrType()
    elif typ == lexer_c.FLOAT:
        return FloatType()
    raise RuntimeError(f"Parse Error: {typ} was NOT A BASE TYPE")


def parse_phrase(lexbuf):
    """
    parse_phrase(lexbuf) creates a list of lists, with the inner lists
    being sections of lexbuf to parse. Applies correct parse to each section
    of list.
    """
    def parse_phrase_helper(lexbuf, tokens, acc):
        # base case
        if lexbuf == []:
            return acc

        # ignore
        # ignore must go first in parsing as it begins with a special amrker
        # that interrupts var parsing
        if lexbuf[0][1] == lexer_c.IGNORE:
            semi_loc = tokens.index(lexer_c.SEMI)
            ignore_statement = lexbuf[0:semi_loc + 1]
            ignore_parsed = parse_ignore(ignore_statement)
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(ignore_parsed)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse union declaration
        if lexbuf[0][1] == lexer_c.UNION:
            semi_loc = tokens.index(lexer_c.SEMI)
            parsed_union = parse_union_declaration(lexbuf[:semi_loc + 1])
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_union)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse struct declaration
        if lexbuf[0][1] == lexer_c.STRUCT:
            l, _ = get_between_brackets(
                lexbuf, 4, lexer_c.OPEN_DICT, lexer_c.CLOSE_DICT)
            semi_loc = tokens[4 + l:].index(lexer_c.SEMI) + (4 + l)
            parsed_struct = parse_struct_declaration(lexbuf[:semi_loc + 1])
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_struct)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse tuple declaraction
        # Tuples are declared as
        # (t1 * t2 * t3) where t could itself be (t1 * t2 * t3)
        if lexbuf[0][1] == lexer_c.LPAREN:
            semi_loc = tokens.index(lexer_c.SEMI)
            l, _ = get_between_brackets(lexbuf, 1)
            tup_typ = parse_tuple_type(
                lexbuf[1:l], lexer_c.TIMES)
            tup_buffer = lexbuf[l + 1:semi_loc]
            parsed_tuple = DeclareTuple(
                tup_typ, parse_assign(tup_buffer))
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_tuple)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse array declaration
        if lexbuf[0][1] == lexer_c.OPEN_ARRAY:
            l, _ = get_between_brackets(
                lexbuf, 1, start=lexer_c.OPEN_ARRAY, end=lexer_c.CLOSE_ARRAY)
            arr_typ = parse_array_type(lexbuf[1:l])
            semi_loc = tokens.index(lexer_c.SEMI)
            list_buffer = lexbuf[l + 1:semi_loc]
            parsed_list = DeclareArray(
                arr_typ, parse_assign(list_buffer))
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_list)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse list declaration
        # lists are declared [type] var := list
        # where type could itself be a list type
        if lexbuf[0][1] == lexer_c.OPEN_BRACKET:
            l, _ = get_between_brackets(
                lexbuf, 1, start=lexer_c.OPEN_BRACKET, end=lexer_c.CLOSE_BRACKET)
            list_typ = parse_list_type(lexbuf[1:l])
            semi_loc = tokens.index(lexer_c.SEMI)
            list_buffer = lexbuf[l + 1:semi_loc]
            parsed_list = DeclareList(
                list_typ, parse_assign(list_buffer))
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_list)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # parse dict declartion: dictionaries are declared as
        # {t1 : t2} var := dictionary
        if lexbuf[0][1] == lexer_c.OPEN_DICT:
            l, _ = get_between_brackets(
                lexbuf, 1, start=lexer_c.OPEN_DICT, end=lexer_c.CLOSE_DICT)
            dict_typ = parse_dict_type(lexbuf[1:l], lexer_c.COLON)
            semi_loc = tokens.index(lexer_c.SEMI)
            dict_buffer = lexbuf[l + 1:semi_loc]
            parsed_dict = DeclareDict(
                dict_typ, parse_assign(dict_buffer))
            new_lex_buff = lexbuf[semi_loc + 1:]
            new_tokens = tokens[semi_loc + 1:]
            acc.append(parsed_dict)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # non custom type declaration
        if lexbuf[0][1] in lexer_c.TYPES:
            end_type_decl = tokens.index(lexer_c.SEMI)
            decl_buff = lexbuf[0:end_type_decl]  # ignore semi
            new_lex_buff = lexbuf[end_type_decl + 1:]
            new_tokens = tokens[end_type_decl + 1:]
            typ = decl_buff[0][1]
            assign_buff = decl_buff[1:]
            parsed_decl = Declaration(
                base_type_to_type_obj(typ), parse_assign(assign_buff))
            acc.append(parsed_decl)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # two consercutve variable types ina  row indicates a custom type
        if len(lexbuf) >= 2 and lexbuf[0][0] == lexer_c.VARIABLE and lexbuf[1][0] == lexer_c.VARIABLE:
            end_type_decl = tokens.index(lexer_c.SEMI)
            decl_buff = lexbuf[0:end_type_decl]  # ignore semi
            new_lex_buff = lexbuf[end_type_decl + 1:]
            new_tokens = tokens[end_type_decl + 1:]
            typ = decl_buff[0][1]
            assign_buff = decl_buff[1:]
            parsed_decl = Declaration(
                CustomType(typ), parse_assign(assign_buff))
            acc.append(parsed_decl)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # assignment must have assign character
        if lexbuf[0][0] == lexer_c.VARIABLE:
            assign_list = []
            new_lex_buff = lexbuf
            new_tokens = tokens
            while (len(new_lex_buff) > 0 and new_lex_buff[0][0] == lexer_c.VARIABLE):
                end_assign = new_tokens.index(lexer_c.SEMI)
                assignment = new_lex_buff[0:end_assign + 1]
                new_lex_buff = new_lex_buff[end_assign + 1:]
                new_tokens = new_tokens[end_assign + 1:]
                assign_list += assignment
            split_buffer = split_lexbuf(assign_list, lexer_c.SEMI)
            assign_list = list(map(lambda l: parse_assign(l), split_buffer))
            acc += assign_list
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # while loop
        if lexbuf[0][1] == lexer_c.WHILE:
            end_while_loc = parse_end(
                lexbuf, 1, lexer_c.WHILE, lexer_c.END_WHILE)
            while_statement = lexbuf[0:end_while_loc + 1]
            while_parsed = parse_while(while_statement)
            new_lex_buff = lexbuf[end_while_loc + 1:]
            new_tokens = tokens[end_while_loc + 1:]
            acc.append(while_parsed)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # if statement
        if lexbuf[0][1] == lexer_c.IF:
            if_pos = 0
            endif_pos = parse_end(lexbuf[1:], 0, lexer_c.IF, lexer_c.ENDIF)

            rem_tokens = tokens[endif_pos + 1:]
            rem_lexbuf = lexbuf[endif_pos + 1:]

            if len(rem_tokens) < 1:
                parsed_if = parse_if_then_else(lexbuf[if_pos:endif_pos + 1])
                acc.append(parsed_if)
                return parse_phrase_helper([], [], acc)

            if rem_tokens[0] != lexer_c.ELIF and rem_tokens[0] != lexer_c.ELSE:
                parsed_if = parse_if_then_else(lexbuf[if_pos:endif_pos + 1])
                acc.append(parsed_if)
                return parse_phrase_helper(rem_lexbuf, rem_tokens, acc)

            endelif_pos = 0
            real_endelif_pos = endif_pos
            while len(rem_tokens) > 0 and rem_tokens[0] == lexer_c.ELIF:
                endelif_pos = parse_end(
                    rem_lexbuf[1:], 0, lexer_c.ELIF, lexer_c.ENDELIF)

                rem_tokens = rem_tokens[endelif_pos + 1:]
                rem_lexbuf = rem_lexbuf[endelif_pos + 1:]
                real_endelif_pos += endelif_pos + 1

            if len(rem_tokens) < 1:
                parsed_if = parse_if_then_else(
                    lexbuf[if_pos:real_endelif_pos + 1])
                acc.append(parsed_if)
                return parse_phrase_helper(rem_lexbuf, rem_tokens, acc)

            if rem_tokens[0] != lexer_c.ELSE:
                parsed_if = parse_if_then_else(
                    lexbuf[if_pos:real_endelif_pos + 1])
                acc.append(parsed_if)
                return parse_phrase_helper(rem_lexbuf, rem_tokens, acc)

            end_else_loc = 0
            real_endelse_loc = real_endelif_pos + 1
            if rem_tokens[0] == lexer_c.ELSE:
                # parse Else
                end_else_loc = parse_end(
                    rem_lexbuf[1:], 0, lexer_c.ELSE, lexer_c.ENDELSE)

                rem_tokens = rem_tokens[end_else_loc + 1:]
                rem_lexbuf = rem_lexbuf[end_else_loc + 1:]

                real_endelse_loc += end_else_loc

            parsed_if = parse_if_then_else(
                lexbuf[if_pos:real_endelse_loc + 1])
            acc.append(parsed_if)
            return parse_phrase_helper(rem_lexbuf, rem_tokens, acc)

        # for loop
        if lexbuf[0][1] == lexer_c.FOR:
            end_for_loc = parse_end(
                lexbuf, 1, lexer_c.FOR, lexer_c.ENDFOR)
            for_statement = lexbuf[0:end_for_loc + 1]
            for_parsed = parse_for(for_statement)
            new_lex_buff = lexbuf[end_for_loc + 1:]
            new_tokens = tokens[end_for_loc + 1:]
            acc.append(for_parsed)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # function
        # parse function type  parsed as
        # fun (t1->t2...->tn) name args ->... where tn is return type
        # and t1 -> t2 -> tn-1 are arg types and
        # there is always one arg type for each arg
        # and always one return type
        if lexbuf[0][1] == lexer_c.FUN:
            # second element is the one after the open bracket
            l, _ = get_between_brackets(
                lexbuf, 2, start=lexer_c.OPEN_TUP, end=lexer_c.CLOSE_TUP)
            func_typ = parse_func_type(lexbuf[2: 1 + l], lexer_c.FUN_ARROW)
            end_fun_loc = parse_end(
                lexbuf, 1, lexer_c.FUN, lexer_c.END_FUN)
            fun_statement = [lexbuf[0]] + lexbuf[2 + l:end_fun_loc + 1]
            fun_parsed = parse_function(fun_statement)
            new_lex_buff = lexbuf[end_fun_loc + 1:]
            new_tokens = tokens[end_fun_loc + 1:]
            num_arg_typs = len(func_typ.get_args_typs())
            num_args = len(fun_parsed.get_args())
            if num_arg_typs != num_args or num_args < 1 or num_arg_typs < 1:
                raise ParseError(
                    "The Number of Function Arguments Should be Equalt o the Number of Function Argument Types, and they Should both be ar least 1 in number.")
            acc.append(DeclareFunc(func_typ, fun_parsed))
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # return
        if lexbuf[0][1] == lexer_c.RETURN:
            end_ret_loc = tokens.index(lexer_c.SEMI)
            ret_statement = lexbuf[0:end_ret_loc + 1]
            ret_parsed = parse_return(ret_statement)
            new_lex_buff = lexbuf[end_ret_loc + 1:]
            new_tokens = tokens[end_ret_loc + 1:]
            acc.append(ret_parsed)
            return parse_phrase_helper(new_lex_buff, new_tokens, acc)

        # error
        raise ParseError("Unrecognized token")

    return parse_phrase_helper(lexbuf, list(map(lambda pair: pair[1], lexbuf)), [])


def split_dict_args(expr_list, split_symbol):
    """
    returns a pair of lists, split at the first instance of split_symbol in
    expr_list

    REQUIRES: expr_list inside of dict or struct cleaned out { or {| and } and |}
    already
    """
    tokens = list(map(lambda pair: pair[1], expr_list))
    # take first as dict cannot be a key, nor can a struct, since both are mutable
    split_pos = tokens.index(split_symbol)
    key_list = expr_list[:split_pos]
    value_list = expr_list[split_pos + 1:]
    return (key_list, value_list)


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
    if elt_typ == lexer_c.INTEGER:
        return 1, IntValue(elt_val)
    elif elt_typ == lexer_c.STRING:
        return 1, StrValue(elt_val)
    elif elt_typ == lexer_c.FLOAT:
        return 1, FloatValue(elt_val)
    elif elt_typ == lexer_c.KEYWORD and (elt_val == lexer_c.TRUE or elt_val == lexer_c.FALSE):
        return 1, BoolValue(True if elt_val == lexer_c.TRUE else False)
    elif elt_val == lexer_c.TAG:
        union_name = lexbuf[1][1]
        assert lexbuf[2][1] == lexer_c.LPAREN
        l, middle_terms = get_between_brackets(lexbuf, 3)
        if middle_terms != []:
            inner_val = parse_expr(middle_terms)
        else:
            inner_val = None
        remainder = lexbuf[l + 3:]
        assert remainder == []
        return (l + 3), UnionValue(union_name, inner_val)
    elif elt_typ == lexer_c.VARIABLE:
        if len(lexbuf) > 1:
            _, la_val = lexbuf[1]
            if la_val == lexer_c.LPAREN:
                # length, middle_terms = get_between_brackets(lexbuf, 2)
                length, middle_terms = get_between_brackets_general(
                    lexbuf, 2, lexer_c.LPAREN, lexer_c.RPAREN)
                split_args = get_function_args(middle_terms, lexer_c.COMMA)
                args_pairs = list(map(lambda args_buffer: parse_expr(
                    args_buffer), split_args))
                args = list(map(lambda pair: pair, args_pairs))
                if elt_val in EXTERNS_LIST:
                    return 2 + length, Extern(elt_val, args)
                return 2 + length, Apply(elt_val, args)
        return 1, VarValue(elt_val)

    # array declaration expression
    elif elt_val == lexer_c.OPEN_ARRAY:
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.OPEN_ARRAY, lexer_c.CLOSE_ARRAY)
        split_args = get_function_args(
            middle_terms, lexer_c.COMMA)
        args_pairs = list(map(lambda args_buffer: parse_expr(
            args_buffer), split_args))
        return 1 + length, Array(args_pairs)
    elif elt_val == lexer_c.CLOSE_ARRAY:
        raise ParseError("Unmatched closing Array symbol")

    elif elt_val == lexer_c.OPEN_TUP:
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.OPEN_TUP, lexer_c.CLOSE_TUP)
        split_args = get_function_args(
            middle_terms, lexer_c.COMMA)
        args_pairs = list(map(lambda args_buffer: parse_expr(
            args_buffer), split_args))
        return 1 + length, Tuple(args_pairs)
    elif elt_val == lexer_c.CLOSE_TUP:
        raise ParseError("Unmatched closing tuple symbol")

    elif elt_val == lexer_c.OPEN_BRACKET:
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.OPEN_BRACKET, lexer_c.CLOSE_BRACKET)
        split_args = get_function_args(
            middle_terms, lexer_c.COMMA)
        args_pairs = list(map(lambda args_buffer: parse_expr(
            args_buffer), split_args))
        return 1 + length, List(args_pairs)
    elif elt_val == lexer_c.CLOSE_BRACKET:
        raise ParseError("Unmatched closing list symbol")

    elif elt_val == lexer_c.OPEN_DICT:
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.OPEN_DICT, lexer_c.CLOSE_DICT)
        split_args = get_function_args(
            middle_terms, lexer_c.COMMA)
        # need to get key values by splitting at lexer_c.COLON
        key_val_list = list(
            map(lambda l: split_dict_args(l, lexer_c.COLON), split_args))
        # key_val_list is a list of pairs, and inside the pairs are lists
        key_list = list(map(lambda pair: pair[0], key_val_list))
        val_list = list(map(lambda pair: pair[1], key_val_list))
        key_args = list(map(lambda args_buffer: parse_expr(
            args_buffer), key_list))
        val_args = list(map(lambda args_buffer: parse_expr(
            args_buffer), val_list))
        return 1 + length, Dict(key_args, val_args)
    elif elt_val == lexer_c.CLOSE_DICT:
        raise ParseError("Unmatched closing dict symbol }")

    elif elt_val == lexer_c.OPEN_STRUCT:
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.OPEN_STRUCT, lexer_c.CLOSE_STRUCT)
        split_args = get_function_args(
            middle_terms, lexer_c.COMMA)
        # need to get key values by splitting at lexer_c.COLON
        key_val_list = list(
            map(lambda l: split_dict_args(l, lexer_c.REV_ARROW), split_args))
        # key_val_list is a list of pairs, and inside the pairs are lists
        key_list = list(map(lambda pair: pair[0], key_val_list))
        val_list = list(map(lambda pair: pair[1], key_val_list))

        for sublist in key_list:
            if len(sublist) != 1:
                raise ParseError("keys for structs must be 1 in length")
            if sublist[0][0] != lexer_c.VARIABLE:
                raise ParseError("keys for structs must be variables")

        key_args = list(map(lambda args_buffer: parse_expr(
            args_buffer), key_list))
        val_args = list(map(lambda args_buffer: parse_expr(
            args_buffer), val_list))
        return 1 + length, Struct(key_args, val_args)
    elif elt_val == lexer_c.CLOSE_STRUCT:
        raise ParseError("Unmatched closing struct symbol |}")

    elif elt_typ == lexer_c.KEYWORD and elt_val in lexer_c.UNOPS:
        _, next_pair = lexbuf[1]
        if next_pair == lexer_c.LPAREN:
            # length, middle_terms = get_between_brackets(lexbuf, 2)
            length, middle_terms = get_between_brackets_general(
                lexbuf, 2, lexer_c.LPAREN, lexer_c.RPAREN)
            parsed_middle_ast = parse_expr(middle_terms)
            return 2 + length, Unop(elt_val, parsed_middle_ast)
        elif next_pair == lexer_c.RPAREN:
            raise UnmatchedParenError(
                "Unmatched right parenthesis %s" % (next_pair))
        elif next_pair == lexer_c.TAG:
            union_name = lexbuf[2][1]
            assert lexbuf[3][1] == lexer_c.LPAREN
            l, middle_terms = get_between_brackets(lexbuf, 4)
            if middle_terms != []:
                inner_val = parse_expr(middle_terms)
            else:
                inner_val = None
            remainder = lexbuf[l + 4:]
            assert remainder == []
            return (l + 3), UnionValue(union_name, inner_val)
        length = 1
        unop_typ, unop_val_ast = lexbuf[1]
        if unop_typ == lexer_c.INTEGER:
            unop_val_ast = IntValue(unop_val_ast)
        elif unop_typ == lexer_c.KEYWORD and (unop_val_ast == lexer_c.TRUE or unop_val_ast == lexer_c.FALSE):
            unop_val_ast = BoolValue(
                True if elt_val == lexer_c.TRUE else False)
        elif unop_typ == lexer_c.VARIABLE:
            unop_val_ast = VarValue(unop_val_ast)
        elif unop_typ == lexer_c.FLOAT:
            unop_val_ast = FloatValue(unop_val_ast)
        return (1 + length), Unop(elt_val, unop_val_ast)

    elif elt_val == lexer_c.LPAREN:
        # length, middle_terms = get_between_brackets(lexbuf, 1)
        length, middle_terms = get_between_brackets_general(
            lexbuf, 1, lexer_c.LPAREN, lexer_c.RPAREN)
        parens_ast = parse_expr(middle_terms)
        return (1 + length), parens_ast
    elif elt_val == lexer_c.RPAREN:
        raise UnmatchedParenError(
            "Unmatched right parenthesis %s" % (elt_val))


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


def split_lexbuf(lexbuf, demarcation):
    def split_lexbuf_helper(lexbuf, demarcation, gather, acc):
        if lexbuf == []:
            return acc

        expr = lexbuf[0]
        remainder = lexbuf[1:]
        if expr[1] != demarcation:
            gather.append(expr)
            return split_lexbuf_helper(remainder, demarcation, gather, acc)

        new_gather = []
        acc.append(gather)
        return split_lexbuf_helper(remainder, demarcation, new_gather, acc)

    return split_lexbuf_helper(lexbuf, demarcation, [], [])


def parse_assign(lexbuf):
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    assign_pos = tokens_list.index(lexer_c.ASSIGN)

    var_list = lexbuf[: assign_pos]
    if len(var_list) != 1:
        raise AssignVariableException(
            " ".join(list(map(lambda pair: str(pair[1]), var_list))) + " is not a variable.")

    var = var_list[0]
    if var[0] != lexer_c.VARIABLE:
        raise AssignVariableException(str(var) + " is not a variable.")

    expr_list = lexbuf[(assign_pos + 1):]
    expr_ast = parse_expr(expr_list)
    return Assign(var[1], expr_ast)


def parse_end(lexbuf, start_loc, start_marker, end_marker):
    def parse_end_helper(lexbuf, length, i, stack, start_marker, end_marker):
        if stack == []:
            return (i)
        if i == length:
            raise ParseError("start marker not ended with end marker")

        _, val = lexbuf[i]
        if val == start_marker:
            stack.append(val)
            return parse_end_helper(lexbuf, len(lexbuf), (i + 1), stack, start_marker, end_marker)
        if val == end_marker:
            if len(stack) >= 1:
                top = stack[0]
                if top == start_marker:
                    stack.pop()
                    return parse_end_helper(lexbuf, len(lexbuf), (i + 1),
                                            stack, start_marker, end_marker)

            stack.append(val)
            return parse_end_helper(lexbuf, len(lexbuf), (i + 1),
                                    stack, start_marker, end_marker)

        return parse_end_helper(lexbuf, len(lexbuf), (i + 1),
                                stack, start_marker, end_marker)

    return parse_end_helper(lexbuf[start_loc:], len(lexbuf[start_loc:]), 0, [start_marker], start_marker, end_marker)


def parse_if_then_else(lexbuf):
    """
    parse_if_then_else(lexbuf) parses
    if guard1 then
        body1
    elseif guard2 then
        body2
    elseif guard3 then
        bod3
    ...
    else
        bodyn
    endif

    with the possibility of
    if guard1 then
        body1
    endif

    of
    if guard1 then
        body1
    else
        body2
    endif

    of
    if guard1 then
        body1
    elseif guard2 then
        body2
    ...
    elseif guardn then
        bodyn
    endif
    """
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    # if is required
    if_pos = tokens_list.index(lexer_c.IF)
    if_then_pos = tokens_list.index(lexer_c.THEN)
    endif_pos = parse_end(lexbuf[1:], 0, lexer_c.IF, lexer_c.ENDIF)

    if_guard = lexbuf[if_pos + 1: if_then_pos]
    if_guard = parse_expr(if_guard)
    if_body = lexbuf[if_then_pos + 1: endif_pos]
    if_body = parse_phrase(if_body)

    rem_tokens = tokens_list[endif_pos + 1:]
    rem_lexbuf = lexbuf[endif_pos + 1:]

    if len(rem_tokens) < 1:
        return IfThenElse(if_guard, if_body, [], [], None)

    elif_guards = []
    elif_bodies = []
    while len(rem_tokens) > 0 and rem_tokens[0] == lexer_c.ELIF:
        elif_then_pos = rem_tokens.index(lexer_c.THEN)
        endelif_pos = parse_end(
            rem_lexbuf[1:], 0, lexer_c.ELIF, lexer_c.ENDELIF)

        guard = rem_lexbuf[1:elif_then_pos]
        body = rem_lexbuf[elif_then_pos + 1:endelif_pos]
        elif_guard = parse_expr(guard)
        elif_body = parse_phrase(body)
        elif_guards.append(elif_guard)
        elif_bodies.append(elif_body)

        rem_tokens = rem_tokens[endelif_pos + 1:]
        rem_lexbuf = rem_lexbuf[endelif_pos + 1:]

    if len(rem_tokens) < 1:
        return IfThenElse(if_guard, if_body, elif_guards, elif_bodies, None)

    else_body = None
    if rem_tokens[0] == lexer_c.ELSE:
        # parse Else
        end_else_loc = parse_end(
            rem_lexbuf[1:], 0, lexer_c.ELSE, lexer_c.ENDELSE)
        else_body = rem_lexbuf[1:end_else_loc]

        if rem_lexbuf[end_else_loc + 1:] != []:
            raise ParseError("Cannot have code after endelse")

        else_body = parse_phrase(else_body)

    return IfThenElse(if_guard, if_body, elif_guards, elif_bodies, else_body)


def parse_while(lexbuf):
    """
    parse_while(lexbuf) parses:
    while expr dowhile:
        phrases...
    endwhile
    as
    While(guard, body)
    """
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    dowhile_pos = tokens_list.index(lexer_c.DO_WHILE)
    endwhile_post = parse_end(lexbuf, 1, lexer_c.WHILE, lexer_c.END_WHILE)
    # endwhile_post = tokens_list.index(lexer_c.END_WHILE)
    while_pos = 0

    guard_list = lexbuf[while_pos + 1:dowhile_pos]
    body_list = lexbuf[dowhile_pos + 1:endwhile_post]

    guard_ast = parse_expr(guard_list)

    body_list_ast = parse_phrase(body_list)

    return While(guard_ast, body_list_ast)


def parse_function(lexbuf):
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    fun_pos = tokens_list.index(lexer_c.FUN)
    fun_arrow_pos = tokens_list.index(lexer_c.FUN_ARROW)
    endfun_pos = parse_end(lexbuf, 1, lexer_c.FUN, lexer_c.END_FUN)

    args_list = lexbuf[fun_pos + 1:fun_arrow_pos]
    if len(args_list) < 1:
        raise ParseError("First Arg must be function name")

    for arg_typ, _ in args_list:
        if arg_typ != lexer_c.VARIABLE:
            raise ParseError("All Args must be variables")

    args_ast_list = list(
        map(lambda arg: parse_expr([arg]), args_list))
    name = args_ast_list[0]
    args_ast_list = args_ast_list[1:]
    body = lexbuf[fun_arrow_pos + 1:endfun_pos]
    body_ast = parse_phrase(body)

    return Function(name, args_ast_list, body_ast)


def parse_return(lexbuf):
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    return_pos = tokens_list.index(lexer_c.RETURN)
    semi_pos = tokens_list.index(lexer_c.SEMI)
    return_body = lexbuf[return_pos + 1:semi_pos]
    body_ast = parse_expr(return_body)
    return Return(body_ast)


def parse_for(lexbuf):
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    for_pos = tokens_list.index(lexer_c.FOR)
    from_pos = tokens_list.index(lexer_c.FROM)
    to_pos = tokens_list.index(lexer_c.TO)
    by_pos = tokens_list.index(lexer_c.BY)
    dofor_pos = tokens_list.index(lexer_c.DOFOR)
    endfor_pos = parse_end(lexbuf, 1, lexer_c.FOR, lexer_c.ENDFOR)

    var = lexbuf[for_pos + 1:from_pos]
    from_int = lexbuf[from_pos + 1:to_pos]
    to_int = lexbuf[to_pos + 1:by_pos]
    by_int = lexbuf[by_pos + 1:dofor_pos]
    body = lexbuf[dofor_pos + 1:endfor_pos]

    if len(var) != 1 or var[0][0] != lexer_c.VARIABLE:
        raise ParseError("Var must be a length 1 variable in For Loop")
    var = parse_expr(var)

    # if len(from_int) != 1 or from_int[0][0] != lexer_c.INTEGER:
    #     raise ParseError("From must be a length 1 INTEGER in For Loop")
    from_int = parse_expr(from_int)

    # if len(to_int) != 1 or to_int[0][0] != lexer_c.INTEGER:
    #     raise ParseError("To must be a length 1 INTEGER in For Loop")
    to_int = parse_expr(to_int)

    # if len(by_int) != 1 or by_int[0][0] != lexer_c.INTEGER:
    #     raise ParseError("By must be a length 1 INTEGER in For Loop")
    by_int = parse_expr(by_int)

    body_list_ast = parse_phrase(body)

    return For(var, from_int, to_int, by_int, body_list_ast)


def parse_ignore(lexbuf):
    tokens_list = list(map(lambda pair: pair[1], lexbuf))
    ignore_pos = tokens_list.index(lexer_c.IGNORE)
    semi_pos = tokens_list.index(lexer_c.SEMI)
    expr = lexbuf[ignore_pos + 1:semi_pos]
    expr_ast = parse_expr(expr)
    return Ignore(expr_ast)


def parse_struct_declaration(lexbuf):
    """
    struct type declaration is
    struct name := {name1:type1;...namen:typen;};
    where n >= 1
    To limit infinite recursion, none of name_i can be the
    name of the struct itself
    though you can have mutual recursion of structs, unions
    and structs and unions
    It is illegal to declare any other type, including a struct, within
    a struct type declaration`
    """
    name_pos = 1
    assign_pos = 2
    open_brace = 3
    assert lexbuf[assign_pos][1] == lexer_c.ASSIGN
    assert lexbuf[0][1] == lexer_c.STRUCT
    assert lexbuf[-1][1] == lexer_c.SEMI
    assert lexbuf[-2][1] == lexer_c.CLOSE_DICT
    assert lexbuf[open_brace][1] == lexer_c.OPEN_DICT
    type_name = lexbuf[name_pos][1]
    tokens_list = list(map(lambda pair: pair[1], lexbuf))

    struct_sub_types = []
    tokens_list = tokens_list[open_brace + 1:]
    lexbuf = lexbuf[open_brace + 1:]
    while lexer_c.SEMI in tokens_list:
        if tokens_list == [lexer_c.CLOSE_DICT, lexer_c.SEMI]:
            break

        semi_pos = tokens_list.index(lexer_c.SEMI)
        struct_type_name = tokens_list[0]

        assert tokens_list[1] == lexer_c.COLON

        struct_type = lexbuf[2:semi_pos]
        struct_type = parse_type(struct_type)

        struct_sub_types.append((struct_type_name, struct_type))

        tokens_list = tokens_list[semi_pos + 1:]
        lexbuf = lexbuf[semi_pos + 1:]

    assert len(struct_sub_types) >= 1

    # structs cannot refer to themselves directly!
    for typ in struct_sub_types:
        assert typ != CustomType(type_name)

    # add subtypes sorted by first element in tuple, a sgtring
    struct_sub_types = sorted(struct_sub_types, key=lambda pair: pair[0])

    return DeclareStruct(type_name, struct_sub_types)


def parse_union_declaration(lexbuf):
    """
    lexbuf begins with "union" keyword 

    lexbuf is the ENTIRE UNION DECLARATION, NO MORE OR NO LESS
    e.g. no extra hanging keywords or characters

    Returns a DeclareUnion type object

    union type is
    union name := A of type1 | B of type 2 |C ...|(typedef declare);
    name var := @A; or name var := @A(2); or ~@B(True);
    union type declaractions CANNOT BE NESTED in each other
    e.f union lol := A of (union lol2 := B of int)) is ILLEGAL
    BUT YOU CAN NEST UNION DECLARATIONS INSIDE OF EACH OTHER
    lol := @A(@B);
    In general, it is illegal to declare any other type including a UNION
    inside a union type declaration

    union always ends with semi colon. there are no possible
    semi colons inside of a union declaration.
    """
    name_pos = 1
    assign_pos = 2
    assert lexbuf[assign_pos][1] == lexer_c.ASSIGN
    assert lexbuf[0][1] == lexer_c.UNION
    type_name = lexbuf[name_pos][1]
    tokens_list = list(map(lambda pair: pair[1], lexbuf))

    union_sub_types = []
    tokens_list = tokens_list[assign_pos + 1:]
    lexbuf = lexbuf[assign_pos + 1:]
    while lexer_c.PIPE in tokens_list:
        pipe_pos = tokens_list.index(lexer_c.PIPE)
        union_type_name = tokens_list[0]

        remainder = lexbuf[1:pipe_pos]
        if remainder == []:
            union_tag_type = None
        else:
            union_tag_type = parse_type(remainder[1:])

        union_sub_types.append((union_type_name, union_tag_type))

        tokens_list = tokens_list[pipe_pos + 1:]
        lexbuf = lexbuf[pipe_pos + 1:]

    semi_pos = tokens_list.index(lexer_c.SEMI)
    union_type_name = tokens_list[0]
    # optional of type statement
    remainder = lexbuf[1:semi_pos]
    if remainder == []:
        union_tag_type = None
    else:
        union_tag_type = parse_type(remainder[1:])

    union_sub_types.append((union_type_name, union_tag_type))

    assert len(union_sub_types) >= 1

    return DeclareUnion(type_name, union_sub_types)


def parse_program(lexbuf):
    return Program(parse_phrase(lexbuf))


if __name__ == "__main__":
    print(parse_phrase(lexer_c.lex(
        "~3;")))
    print(parse_phrase(lexer_c.lex(
        "~print();")))

    print(parse_phrase(lexer_c.lex(
        '~(|(|(3 + 4), x, y|), 3,(4 + 5), unit((|("hi")|))|);')))
    print(parse_phrase(lexer_c.lex("int x := 3; int y := 4;")))
    print(parse_phrase(lexer_c.lex(
        "(bool * int * ((int * int) * int) * float) t := (|1, 2|);")))
    pass

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "((-1 * -1) + 4 * y * z * 3 * 2) * (7 + 4 * 5 *6)")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f (3, 4)")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "3 + 3*4  + 5*6 + 7*8**9")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "3 + unitary () ** -156")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "3 + unitary () * 2 * 3 * 4")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "3 + 3 * unitary () + 2 * 3 * 4")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "2 + (3 * 5) * 4 * 3 * 2")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f(g(2, 3), 2)")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f(g(2, 3), h(4), 3, (2 + 3), x, g(x, h(m(d, 100), z)))")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "1 - -(3 - (3 + 4) * 2 + 4)")))

    # # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    # #     "3 -1 * (2 * 3) * 4")))

    # print(parse_phrase(lexer_c.lex("x := 3; y := 2 + (3 * 5) * 4 * 3 * 2;")))
    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; if x + 1 then x := 3; endif while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_program(lexer_c.lex(
    #     "x := 1; while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_while(lexer_c.lex("while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile")))
    # print(parse_if_then_else(lexer_c.lex("if x + 1 then x := 1; y := 2; endif")))
    # print(parse_if_then_else(
    #     lexer_c.lex("if x + 1 then x := 1; y := 2; endif else y := -4; endelse")))
    # print(parse_if_then_else(
    #     lexer_c.lex("if x + 1 then x := 1; endif else y := -4; endelse")))
    # print(parse_if_then_else(
    #     lexer_c.lex("if x + 1 then x := 1; endif elif x - 2 then x := 2 ** 2; endelif else y := -4; endelse")))
    # print(parse_if_then_else(
    #     lexer_c.lex("if x + 1 then x := 1; endif elif x - 2 then x := 2 ** 2; endelif elif y - -4 then q := -2 ** 2; endelif else y := -4; endelse")))
    # print(parse_if_then_else(
    #     lexer_c.lex("if x + 1 then x := 1; endif elif x - 2 then x := 2 ** 2; endelif elif y - -4 then q := -2 ** 2; endelif")))

    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; if x + 1 then x := 3; endif elif y -2 then y := 100; endelif while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; if x + 1 then x := 3; endif elif y -2 then y := 100; endelif else k := 40; endelse while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; if x + 1 then x := 3; endif elif y -2 then y := 100; endelif elif y -2 then y := 100; endelif elif y -2 then y := 100; endelif else k := 40; endelse while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))
    # print(parse_phrase(lexer_c.lex(
    #     "x := 1; if x + 1 then x := 3; endif else k := 40; endelse while x + 1 dowhile y := 3; z := 4; x := x - 1;endwhile x := 2;")))

    # # embedding
    # print(parse_phrase(lexer_c.lex(
    #     "if x + 1 then if x + 1 then x :=4; endif elif x then x :=5; endelif else if z then z := 4; endif endelse endif else k := 40; endelse")))
    # print(parse_phrase(lexer_c.lex(
    #     "while x dowhile while y dowhile x := x + y; endwhile while z dowhile z := z + 1;endwhile endwhile")))
    # print(parse_phrase(lexer_c.lex(
    #     "while x dowhile if x then x := 4;endif endwhile")))
    # print(parse_phrase(lexer_c.lex(
    #     "if x then while x dowhile x := x + 1; endwhile endif")))

    # # for loops
    # print(parse_phrase(lexer_c.lex(
    #     "for x from 1 to 3 by 1 dofor x := 4; endfor")))
    # print(parse_phrase(lexer_c.lex(
    #     "for x from 1 to 3 by 1 dofor for i from -100 to 20 by z * z dofor l := -1; endfor k := l + 1;  endfor")))
    # print(parse_phrase(lexer_c.lex(
    #     "for x from 1 to 3 by 1 dofor if x then y := y + 1; endif k := l + 1;  endfor")))

    # # functions
    # print(parse_phrase(lexer_c.lex(
    #     "fun f x y -> x := x + y; endfun")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f x -> x := x + y; endfun")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f-> x := x + y; endfun")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f-> while x dowhile x := x + 1; endwhile endfun")))

    # # return
    # print(parse_phrase(lexer_c.lex(
    #     "return x * x + 3;")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f x y -> x := x + y; return x; endfun")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f x y -> x := x + y; return ; endfun")))
    # print(parse_phrase(lexer_c.lex(
    #     "fun f x y -> x := x + y; if x then return ; endif endfun")))

    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f((3 + 3))")))
    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f(-3)")))
    # print(parse_expr(1, 0, 1, [], lexer_c.lex(
    #     "f(3 * 3, 2)")))
