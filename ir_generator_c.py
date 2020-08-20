"""
ir_generator_c is a ir generator from the c-like code language to
the lower level RISC-like language
"""


# ---------- LANGUAGE IMPORTS -------------
import lexer_c
import ast_generator_c
import type_check_c


# ---------- IR OP CODE CONSTANTS --------
ADD = "add"
ADDI = "addi"
THROWAWAY_REG = "x31"  # meant to be reused immediately
ZERO = "x0"
N_REGISTERS = 32
REGISTER_DICT = {f"x{i}": None for i in range(1, N_REGISTERS - 1)}


# --------- IR OP CODE NAMES -------------
ADD = "add"
SUB = "sub"
MULT = "mult"
DIV = "div"
LOAD = "load"
STORE = "store"
LABEL = "label"
LI = "load_immediate"


# ---------- INFORMATION CLASSES ---------
class Mappings():
    def __init__(self, reg_map, sym_table):
        self.reg_map = reg_map
        self.sym_table = sym_table
        self.throwaway = False

    def set_reg_map(self, reg_map):
        self.reg_map = reg_map

    def set_sym_table(self, sym_table):
        self.sym_table = sym_table

    def get_reg_map(self):
        return self.reg_map

    def get_sym_table(self):
        return self.sym_table

    def get_throwaway(self):
        return self.throwaway

    def set_throwaway(self, val):
        self.throwaway = val

    def get_reg(self):
        return "x30"


# ---------- IR CLASSES ------------------
class IntImm():
    def __init__(self, int_val):
        self.val = int_val


class GenAdd():
    def __init__(self, bop, rd, rs1, rs2):
        self.bop = bop
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def get_bop(self):
        return self.bop

    def get_rs1(self):
        return self.rs1

    def get_rs2(self):
        return self.rs2

    def get_rd(self):
        return self.rd


def gen_int(_int, mapping, cmd_stack):
    assert type(_int) == ast_generator_c.IntValue
    val = _int.get_value()
    mapping.set_throwaway(True)
    cmd = (LI, THROWAWAY_REG, val)
    cmd_stack.append(cmd)


def gen_add_int(add_int, mapping, cmd_stack):
    """
    gen_add_int(add_int_node, mapping, cmd_stack) generates IR AST node code for
    a add_int_node.

    Returns IR Ast Node

    Add_int_node must be syntactically correct under type checking
    """
    left_node = add_int.get_left()
    gen_expr(left_node, mapping, cmd_stack)
    if mapping.get_throwaway():
        reg = mapping.get_reg()
        cmd = (ADD, reg, THROWAWAY_REG, ZERO)
        cmd_stack.append(cmd)
        mapping.set_throwaway(False)
    right_node = add_int.get_right()
    gen_expr(right_node, mapping, cmd_stack)
    if mapping.get_throwaway():
        reg = mapping.get_reg()
        cmd = (ADD, reg, THROWAWAY_REG, ZERO)
        cmd_stack.append(cmd)
        mapping.set_throwaway(False)


def gen_binop(bop, mapping, cmd_stack):
    op = bop.get_bop()
    if op == lexer_c.PLUS:
        return gen_add_int(bop, mapping, cmd_stack)


def gen_expr(expr, mapping, cmd_stack):
    if type(expr) == ast_generator_c.IntValue:
        return gen_int(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Bop:
        return gen_binop(expr, mapping, cmd_stack)


def gen_ignore(ignore, mapping, cmd_stack):
    expr = ignore.get_expr()
    return gen_expr(expr, mapping, cmd_stack)


def gen_phrase(phrase, mapping, cmd_stack):
    if type(phrase) == ast_generator_c.Ignore:
        return gen_ignore(phrase, mapping, cmd_stack)


def gen_program(program):
    cmd_stack = []
    reg_map = REGISTER_DICT
    sym_table = {}
    mapping = Mappings(reg_map, sym_table)

    phrases = program.get_phrases()
    for phrase in phrases:
        gen_phrase(phrase, mapping, cmd_stack)

    return cmd_stack


if __name__ == "__main__":
    program = r"~3 + 4;"
    print(gen_program(ast_generator_c.parse_program(lexer_c.lex(program))))


# Notes
# When generating, there are n registers n >= 1 and I will store
# data in one register and keep shifting data to a free register.
