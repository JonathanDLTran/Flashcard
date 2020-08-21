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
BACKUP_REG = "x30"  # meant to be used as an intermediate with the throwaway
ZERO = "x0"
N_REGISTERS = 32
REGISTER_DICT = {f"x{i}": None for i in range(1, N_REGISTERS - 2)}
STACK_LOC = 'stack_loc'


# --------- IR OP CODE NAMES -------------
ADD = "add"
SUB = "sub"
MUL = "mul"
DIV = "div"
NOT = "not"
LOAD = "load"
STORE = "store"
LABEL = "label"
LI = "load_immediate"
MV = "move"
JAL = "jal"
JALR = "jalr"
BEQ = "beq"
BNE = "bne"
BGE = "bge"
BLT = "blt"


# ---------- INFORMATION CLASSES ---------
class Mappings():
    def __init__(self, reg_map, sym_table):
        self.reg_map = reg_map
        self.rev_reg_map = {reg_map[key]: key for key in reg_map}
        self.sym_table = sym_table
        self.throwaway = False
        self.while_idx = 1
        self.for_idx = 1

    def set_reg_map(self, reg_map):
        self.reg_map = reg_map

    def set_rev_reg_map(self, rev_reg_map):
        self.rev_reg_map = rev_reg_map

    def set_sym_table(self, sym_table):
        self.sym_table = sym_table

    def set_while_idx(self, idx):
        self.while_idx = idx

    def set_for_idx(self, idx):
        self.for_idx = idx

    def get_reg_map(self):
        return self.reg_map

    def get_sym_table(self):
        return self.sym_table

    def get_rev_reg_map(self):
        return self.rev_reg_map

    def get_while_idx(self):
        return self.while_idx

    def get_for_idx(self):
        return self.for_idx

    def get_reg(self, var_name):
        reg_map = self.reg_map
        for reg in reg_map:
            if reg_map[reg] == None:
                reg_map[reg] = var_name
                rev_reg_map = {reg_map[key]: key for key in reg_map}
                self.set_rev_reg_map(rev_reg_map)
                return reg
        raise KeyError("No more free registers. ")


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
    cmd = (LI, THROWAWAY_REG, val)
    cmd_stack.append(cmd)


def gen_int_op(int_op, op, mapping, cmd_stack):
    """
    gen_int_op(add_int_node, op, mapping, cmd_stack) generates IR AST node code for
    a int_op node.

    Returns IR Ast Node

    int_op must be syntactically correct under type checking
    """
    def op_to_code(op):
        trans_dict = {lexer_c.PLUS: ADD, lexer_c.MINUS: SUB,
                      lexer_c.TIMES: MUL, lexer_c.DIV: DIV, }
        return trans_dict[op]

    left_node = int_op.get_left()
    gen_expr(left_node, mapping, cmd_stack)
    cmd = (ADD, BACKUP_REG, THROWAWAY_REG, ZERO)
    cmd_stack.append(cmd)
    right_node = int_op.get_right()
    gen_expr(right_node, mapping, cmd_stack)
    cmd = (op_to_code(op), BACKUP_REG, BACKUP_REG, THROWAWAY_REG)
    cmd_stack.append(cmd)
    cmd = (MV, THROWAWAY_REG, BACKUP_REG)
    cmd_stack.append(cmd)


def gen_binop(bop, mapping, cmd_stack):
    op = bop.get_bop()
    if op in [lexer_c.PLUS, lexer_c.MINUS, lexer_c.TIMES, lexer_c.DIV]:
        return gen_int_op(bop, op, mapping, cmd_stack)


def gen_expr(expr, mapping, cmd_stack):
    if type(expr) == ast_generator_c.IntValue:
        return gen_int(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Bop:
        return gen_binop(expr, mapping, cmd_stack)


def gen_ignore(ignore, mapping, cmd_stack):
    expr = ignore.get_expr()
    return gen_expr(expr, mapping, cmd_stack)


def gen_assign(assign, mapping, cmd_stack):
    expr = assign.get_expr()
    var = assign.get_var()

    if var not in mapping.get_rev_reg_map():
        reg = mapping.get_reg(var)
    else:
        reg = mapping.get_rev_reg_map()[var]

    gen_expr(expr, mapping, cmd_stack)
    cmd = (ADD, reg, THROWAWAY_REG, ZERO)
    cmd_stack.append(cmd)


def gen_declaration(declr, mapping, cmd_stack):
    assign = declr.get_assign()
    return gen_assign(assign, mapping, cmd_stack)


def gen_while(_while, mapping, cmd_stack):
    """
    while_header_ix:
    negative assembly condition jump to while_footer_idx
    (NOT rd, rs)
    add while guard condition
    while loop body
    beq x0, x0, while_header_ix
    while_footer_idx:
    """
    guard = _while.get_guard()
    body = _while.get_body()

    # add while header
    while_idx = mapping.get_while_idx()
    mapping.set_while_idx(while_idx + 1)

    while_header = f"while_header_{while_idx}"
    cmd = (LABEL, while_header)
    cmd_stack.append(cmd)

    # negate guard condition
    gen_expr(guard, mapping, cmd_stack)
    cmd = (NOT, THROWAWAY_REG, THROWAWAY_REG)
    cmd_stack.append(cmd)

    # add the guard condition
    while_footer = f"while_footer_{while_idx}"
    cmd = (BEQ, THROWAWAY_REG, ZERO, while_footer)
    cmd_stack.append(cmd)

    # generate body of while loop
    for phrase in body:
        gen_phrase(phrase, mapping, cmd_stack)

    # add in absolute branch to header
    cmd = (BEQ, ZERO, ZERO, while_header)
    cmd_stack.append(cmd)

    # generate while footer
    cmd = (LABEL, while_footer)
    cmd_stack.append(cmd)

    return


def gen_for(_for, mapping, cmd_stack):
    """
    set for variable
    for_header_idx:
    negate for guard condition 
    add for guard branch
    for body
    increment for variable
    branch to for header
    for_footer_idx:
    """
    index_var = _for.get_index().get_value()
    _from = _for.get_from().get_value()
    _end = _for.get_end().get_value()
    _by = _for.get_by().get_value()
    body = _for.get_body()

    # add for variable
    if index_var not in mapping.get_rev_reg_map():
        reg = mapping.get_reg(index_var)
    else:
        reg = mapping.get_rev_reg_map()[index_var]

    cmd = (LI, reg, _from)
    cmd_stack.append(cmd)

    # add for header
    for_idx = mapping.get_for_idx()
    mapping.set_for_idx(for_idx + 1)

    for_header = f"for_header_{for_idx}"
    cmd = (LABEL, for_header)
    cmd_stack.append(cmd)

    # negate guard condition
    for_footer = f"for_footer_{for_idx}"

    # add x31, var, x0
    cmd = (ADD, THROWAWAY_REG, reg, ZERO)
    cmd_stack.append(cmd)

    # LI x30, _end
    cmd = (LI, BACKUP_REG, _end)
    cmd_stack.append(cmd)

    # add in guard branch
    if _from < _end:
        # BGE var, _end, for_footer
        cmd = (BGE, THROWAWAY_REG, BACKUP_REG, for_footer)
        cmd_stack.append(cmd)
    else:
        # BGE var, _end, for_footer
        cmd = (BLT, THROWAWAY_REG, BACKUP_REG, for_footer)
        cmd_stack.append(cmd)

    # for body
    for phrase in body:
        gen_phrase(phrase, mapping, cmd_stack)

    # increment for variable
    cmd = (ADD, reg, reg, IntImm(_by))
    cmd_stack.append(cmd)

    # branch to header
    cmd = (BEQ, ZERO, ZERO, for_header)
    cmd_stack.append(cmd)

    # for footer
    cmd = (LABEL, for_footer)
    cmd_stack.append(cmd)

    return


def gen_phrase(phrase, mapping, cmd_stack):
    if type(phrase) == ast_generator_c.Ignore:
        return gen_ignore(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.Declaration:
        return gen_declaration(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.Assign:
        return gen_assign(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.While:
        return gen_while(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.For:
        return gen_for(phrase, mapping, cmd_stack)


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
    program = r"~3 + 4;~3 - 4; int x := 3; x:= 2; while True dowhile x := 1; endwhile for i from 1 to 3 by 1 dofor x := 1; endfor"
    print(
        gen_program(
            type_check_c.type_check(
                ast_generator_c.parse_program(
                    lexer_c.lex(program)))))


# Notes
# When generating, there are n registers n >= 1 and I will store
# data in one register and keep shifting data to a free register.
