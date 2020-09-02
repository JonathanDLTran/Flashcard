"""
riscv_emit_c is a ir generator from the c-like code language to
the lower level RISC-like language
"""


# ---------- LANGUAGE IMPORTS -------------
import lexer_c
import ast_generator_c
import type_check_c


# ---------- OTHER IMPORTS --------------
from copy import deepcopy


# ---------- DATA SIZES -----------------
INT = "int"
CHAR = "char"
FLOAT = "float"
SIZEOF = {INT: 4, CHAR: 1, FLOAT: 8, }


# ---------- OTHER SIZE UTILITIES ----------------------------------------
def round_to_closest_pow(base, num):
    """
    rounds num to closest power of [base]
    """
    power = 1
    while base ** power < num:
        power += 1
    return base ** power


def sizeof(typ):
    if type(typ) == ast_generator_c.IntType:
        return SIZEOF[INT]
    elif type(typ) == ast_generator_c.DeclareStruct:
        typ_list = typ.get_typ_list()
        sizes_list = list(map(lambda t: sizeof(t), typ_list))
        rounded_sizes = list(
            map(lambda s: round_to_closest_pow(2, s), sizes_list))
        return sum(rounded_sizes)
    elif type(typ) == ast_generator_c.DeclareUnion:
        typ_list = typ.get_typ_list()
        sizes_list = list(map(lambda t: sizeof(t), typ_list))
        return max(sizes_list)
    elif type(typ) == ast_generator_c.TupleType:
        typ_list = typ.get_typ_list()
        sizes_list = list(map(lambda t: sizeof(t), typ_list))
        rounded_sizes = list(
            map(lambda s: round_to_closest_pow(2, s), sizes_list))
        return sum(rounded_sizes)


# ---------- IR REGISTER CONSTANTS --------
N_REGISTERS = 32

ZERO = "x0"
RA = "x1"
SP = "x2"
GP = "x3"
TP = "x4"
FP = "x8"
BACKUP_REG = "x30"  # meant to be used as an intermediate with the throwaway
THROWAWAY_REG = "x31"  # meant to be reused immediately

ALL_REGISTERS = [f"x{i}" for i in range(N_REGISTERS)]
SPECIAL_REGS = {RA, SP, GP, TP, FP, THROWAWAY_REG, BACKUP_REG, ZERO}

START_REG_VAR_MAP = {f"x{i}": None for i in range(N_REGISTERS)}

START_STACK = int("0x70000000", 16)


# --------- IR OP CODE NAMES -------------
ADD = "add"
ADDI = "addi"
AND = "and"
ANDI = "andi"
SUB = "sub"
MUL = "mul"
DIV = "div"
NOT = "not"
LW = "load_word"
SW = "store_word"
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
    def __init__(self, reg_var_map, var_stack_map, closure_vars, old_closure_vars):
        """
        A Mappings object contains the state needed for the translation in a single
        stack frame

        A Mappings object is created each time a function is cdefined/declared
        """

        # indicdes to mark headers and footers for jumping
        # to while, for, if and functions
        self.while_idx = 1
        self.for_idx = 1
        self.if_idx = 1
        self.curr_func = None

        # reg_var_map maps each register to None or a string, the name of a variable
        self.reg_var_map = reg_var_map
        # var_stack_map maps each variable to a location on the stack relative
        # to the stack pointer, e.g.  40 + SP
        self.var_stack_map = var_stack_map

        # this is an ordered list of  closure vars in that order
        # with first being the top most and last being bottom most ons tack
        self.closure_vars_ordered = old_closure_vars

        # mappings is the mappings inside the function for
        # different functiond
        # it is in the form {<"function name"> : mapping_obj}
        self.mappings = {}

        # closure_vars is the list of all closure variables for this stakc frame
        # including those varibales it inherited from a previous stack frame
        self.closure_vars = closure_vars

    def set_reg_map(self, reg_map):
        self.reg_map = reg_map

    def set_rev_reg_map(self, rev_reg_map):
        self.rev_reg_map = rev_reg_map

    def set_while_idx(self, idx):
        self.while_idx = idx

    def set_for_idx(self, idx):
        self.for_idx = idx

    def set_if_idx(self, idx):
        self.if_idx = idx

    def set_curr_func(self, func_name):
        self.curr_func = func_name

    def set_mappings(self, mappings):
        self.mappings = mappings

    def get_reg_map(self):
        return self.reg_map

    def get_rev_reg_map(self):
        return self.rev_reg_map

    def get_while_idx(self):
        return self.while_idx

    def get_for_idx(self):
        return self.for_idx

    def get_if_idx(self):
        return self.if_idx

    def get_curr_func(self):
        return self.curr_func

    def get_reg_var_map(self):
        return self.reg_var_map

    def get_var_stack_map(self):
        return self.var_stack_map

    def get_mappings(self):
        return self.mappings

    def get_closure_vars(self):
        return self.closure_vars

    def get_old_closure_vars(self):
        return self.closure_vars_ordered


# ---------- FUNCTION STACK FRAME ANALYSIS -------------------------


def get_all_vars(phrases):
    """
    get_all_vars(function_body) gets a unique set of variables
    used in a function_body and returns a list of those string names of
    the variables

    USED FOR CALLING CONVENTION IN STACK FRAME TO RESERVE MEMORY FOR EACH VARIABLE
    """
    # assert type(function_body) == ast_generator_c.Program

    # phrases = function_body.get_phrases()

    vars_list = []
    for phrase in phrases:
        if type(phrase) == ast_generator_c.Ignore:
            pass  # cannot declare a variable
        elif type(phrase) == ast_generator_c.Declaration:
            assign = phrase.get_assign()
            var = assign.get_var()
            vars_list.append(var)
        elif type(phrase) == ast_generator_c.Assign:
            var = phrase.get_var()
            vars_list.append(var)
        elif type(phrase) == ast_generator_c.While:
            body = phrase.get_body()
            inner_vars = get_all_vars(body)
            vars_list += inner_vars
        elif type(phrase) == ast_generator_c.For:
            index_var = phrase.get_index().get_value()
            vars_list.append(index_var)
            body = phrase.get_body()
            inner_vars = get_all_vars(body)
            vars_list += inner_vars
        elif type(phrase) == ast_generator_c.IfThenElse:
            (_, if_body) = phrase.get_if_pair()
            (_, elif_bodies) = phrase.get_elif_pair_list()
            else_body = phrase.get_else()

            inner_vars = get_all_vars(if_body)
            vars_list += inner_vars

            for elif_body in elif_bodies:
                inner_vars = get_all_vars(elif_body)
                vars_list += inner_vars

            if else_body != None:
                inner_vars = get_all_vars(else_body)
                vars_list += inner_vars

        elif type(phrase) == ast_generator_c.DeclareFunc:
            pass  # new scope
        elif type(phrase) == ast_generator_c.Return:
            pass  # cannot declare a variable
        elif type(phrase) == ast_generator_c.DeclareArray:
            assign = phrase.get_assign()
            var = assign.get_var()
            vars_list.append(var)
    return list(set(vars_list))


# ---------- REGISTER REPLACEMENT ALGORITHMS ------------------


def reg_to_boot(reg_var_map):
    """
    reg_to_boot(reg_var_map) boots the first register in reg_var_map

    reg_var_map must have at least one register

    TODO: OPTIMIZE REPLACEMNT ALGORITHM
    """
    for reg in reg_var_map:
        if reg not in SPECIAL_REGS:
            return reg


def move_var_to_reg(reg_var_map, var_stack_map, var, cmd_stack):
    """
    move_var_to_reg(reg_var_map, var_stack_map, var, cmd_stack) moves var
    to a register in reg_var_map

    if extra commands have to be used to load and store,
    commands are added automatically to the command stakc
    """

    # check if var is already bound to a register
    for reg, _var in reg_var_map.items():
        if _var == var:
            return reg

    # check if there is an open register
    for reg, _var in reg_var_map.items():
        if reg not in SPECIAL_REGS:
            if _var == None:
                return reg

    # no free registers: boot some variable from a register
    boot_reg = reg_to_boot(reg_var_map)
    add_var_to_reg(reg_var_map, var_stack_map, var, boot_reg, cmd_stack)

    return boot_reg


def add_var_to_reg(reg_var_map, var_stack_map, var, reg, cmd_stack):
    """
    add_var_to_reg(reg_var_map, var_stack_map, var, reg, cmd_stack) assumes var is not bound
    to a register in reg_var_map
    """

    # remove the var from register and spill into stack
    old_var = reg_var_map[reg]
    old_var_loc = var_stack_map[old_var]

    cmd = (LI, THROWAWAY_REG, old_var_loc)
    cmd_stack.append(cmd)

    cmd = (SW, reg, 0, THROWAWAY_REG)
    cmd_stack.append(cmd)

    # add var from stack to register
    reg_var_map[reg] = var
    new_var_loc = var_stack_map[var]

    cmd = (LI, THROWAWAY_REG, new_var_loc)
    cmd_stack.append(cmd)

    cmd = (LW, reg, 0, THROWAWAY_REG)
    cmd_stack.append(cmd)


# ----------- CODE GENERATION -----------------


def gen_int(_int, mapping, cmd_stack):
    """
    gen_int(_int, mapping, cmd_stack) places the int in THROWAWAY_REG
    and returns THROWAWAY_REG

    REQUIRES: BACKUP_REG and THROWAWAY_REG are held free for these operations
    RETURNS: REGISTER
    """
    assert type(_int) == ast_generator_c.IntValue
    val = _int.get_value()
    cmd = (LI, THROWAWAY_REG, val)
    cmd_stack.append(cmd)

    return THROWAWAY_REG


def gen_bool(_bool, mapping, cmd_stack):
    """
    gen_bool(_bool, mapping, cmd_stack) places the int in THROWAWAY_REG
    and returns THROWAWAY_REG

    REQUIRES: BACKUP_REG and THROWAWAY_REG are held free for these operations
    RETURNS: REGISTER
    """
    assert type(_bool) == ast_generator_c.BoolValue
    val = _bool.get_value()
    if val:
        cmd = (LI, THROWAWAY_REG, 1)
    else:
        cmd = (LI, THROWAWAY_REG, 0)
    cmd_stack.append(cmd)

    return THROWAWAY_REG


def gen_int_op(int_op, op, mapping, cmd_stack):
    """
    gen_int_op(add_int_node, op, mapping, cmd_stack) generates IR AST node code for
    a int_op node.

    Returns THROWAWAY_REG which holds the result of the int op
    RETURNS: REGISTER
    REQUIRES: BACKUP_REG and THROWAWAY_REG are held free for these operations

    int_op must be syntactically correct under type checking
    """
    def op_to_code(op):
        trans_dict = {lexer_c.PLUS: ADD, lexer_c.MINUS: SUB,
                      lexer_c.TIMES: MUL, lexer_c.DIV: DIV, }
        return trans_dict[op]

    left_node = int_op.get_left()
    left_reg = gen_expr(left_node, mapping, cmd_stack)
    cmd = (ADD, BACKUP_REG, left_reg, ZERO)
    cmd_stack.append(cmd)
    right_node = int_op.get_right()
    right_reg = gen_expr(right_node, mapping, cmd_stack)
    cmd = (op_to_code(op), BACKUP_REG, BACKUP_REG, right_reg)
    cmd_stack.append(cmd)
    cmd = (MV, THROWAWAY_REG, BACKUP_REG)
    cmd_stack.append(cmd)

    return THROWAWAY_REG


def gen_var(var, mapping, cmd_stack):
    """
    gen_var is the register bound to var

    RETURNS: REGISTER
    """
    var_name = var.get_value()
    return move_var_to_reg(mapping.get_reg_var_map(), mapping.get_var_stack_map(), var_name, cmd_stack)


def gen_binop(bop, mapping, cmd_stack):
    """
    gen_binop(bop, mapping, cmd_stack) gens assembly code for the bop
    and returns what register the binary operastion result is stored in

    RETURNS: REGISTER
    """
    op = bop.get_bop()
    if op in [lexer_c.PLUS, lexer_c.MINUS, lexer_c.TIMES, lexer_c.DIV]:
        return gen_int_op(bop, op, mapping, cmd_stack)


def gen_apply(apply, mapping, cmd_stack):
    """
    gen_apply
    loads in the arguments below the SP
    then jal to ra, label
    """
    func_name = apply.get_fun()
    func_args = apply.get_args()

    curr_var_stack_mapping = mapping.get_var_stack_map()

    mappings_dict = mapping.get_mappings()
    func_mapping = mappings_dict[func_name]
    func_closure_vars = func_mapping.get_old_closure_vars()

    # load in incoming args at SP and BELOW
    i = 0
    func_args.reverse()
    for arg_expr in func_args:
        arg_reg = gen_expr(arg_expr, mapping, cmd_stack)
        new_loc = -1 * i * SIZEOF[INT]
        cmd = (SW, arg_reg, new_loc, SP)
        cmd_stack.append(cmd)
        i += 1

    # load in closure args below incking args
    func_closure_vars.reverse()
    for closure_var in func_closure_vars:
        curr_stack_loc = curr_var_stack_mapping[closure_var]
        cmd = (LW, THROWAWAY_REG, curr_stack_loc, SP)
        cmd_stack.append(cmd)
        new_loc = -1 * i * SIZEOF[INT]
        cmd = (SW, THROWAWAY_REG, new_loc, SP)
        cmd_stack.append(cmd)
        i += 1

    # jal to func_name
    func_header = f"{func_name}_header"
    cmd = (JAL, RA, func_header)
    cmd_stack.append(cmd)


def gen_int_unop(unop, op, mapping, cmd_stack):
    if op == lexer_c.MINUS:
        expr = unop.get_expr()
        reg = gen_expr(expr, mapping, cmd_stack)
        cmd = (SUB, reg, ZERO, reg)
        cmd_stack.append(cmd)
        return reg


def gen_bool_unop(unop, op, mapping, cmd_stack):
    if op == lexer_c.NOT:
        expr = unop.get_expr()
        reg = gen_expr(expr, mapping, cmd_stack)

        # turn 1 to 0 and 0 to 1 with NOT complement and bit mask
        cmd = (NOT, reg, reg)
        cmd_stack.append(cmd)

        cmd = (ANDI, reg, reg, 1)
        cmd_stack.append(cmd)
        return reg


def gen_unop(unop, mapping, cmd_stack):
    op = unop.get_unop()
    if op == lexer_c.MINUS:
        return gen_int_unop(unop, op, mapping, cmd_stack)
    elif op == lexer_c.NOT:
        return gen_bool_unop(unop, op, mapping, cmd_stack)


def gen_array(array, mapping, cmd_stack):
    pass


def gen_expr(expr, mapping, cmd_stack):
    if type(expr) == ast_generator_c.IntValue:
        return gen_int(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.BoolValue:
        return gen_bool(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.VarValue:
        return gen_var(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Array:
        return gen_array(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Unop:
        return gen_unop(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Bop:
        return gen_binop(expr, mapping, cmd_stack)
    elif type(expr) == ast_generator_c.Apply:
        return gen_apply(expr, mapping, cmd_stack)


def gen_ignore(ignore, mapping, cmd_stack):
    expr = ignore.get_expr()
    return gen_expr(expr, mapping, cmd_stack)


def gen_assign(assign, mapping, cmd_stack):
    expr = assign.get_expr()
    var = assign.get_var()

    reg = move_var_to_reg(mapping.get_reg_var_map(),
                          mapping.get_var_stack_map(), var, cmd_stack)

    expr_reg = gen_expr(expr, mapping, cmd_stack)
    cmd = (ADD, reg, expr_reg, ZERO)
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
    guard_reg = gen_expr(guard, mapping, cmd_stack)
    cmd = (NOT, guard_reg, guard_reg)
    cmd_stack.append(cmd)

    # add the guard condition
    while_footer = f"while_footer_{while_idx}"
    cmd = (BEQ, guard_reg, ZERO, while_footer)
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
    reg = move_var_to_reg(mapping.get_reg_var_map(),
                          mapping.get_var_stack_map(), index_var, cmd_stack)

    # if index_var not in mapping.get_rev_reg_map():
    #     reg = mapping.get_reg(index_var)
    # else:
    #     reg = mapping.get_rev_reg_map()[index_var]

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
    cmd = (ADDI, reg, reg, _by)
    cmd_stack.append(cmd)

    # branch to header
    cmd = (BEQ, ZERO, ZERO, for_header)
    cmd_stack.append(cmd)

    # for footer
    cmd = (LABEL, for_footer)
    cmd_stack.append(cmd)


def gen_if_then_else(ifthenelse, mapping, cmd_stack):
    """
    if_header_ix:
    negative assembly condition jump to if_footer_idx
    (NOT rd, rs)
    add if guard condition
    if body
    beq x0, x0, end_if_then_else_idx
    if_footer_idx:

    elif_header_idx_1:
    negative assembly condition jump to elif_footer_idx_1
    (NOT rd, rs)
    add elif 1 guard condition
    elif 1 body
    beq x0, x0, end_if_then_else_idx
    elif_footer_idx_1:

    ... more elifs

    else body

    end_if_then_else_idx
    """
    (if_guard, if_body) = ifthenelse.get_if_pair()
    (elif_guards, elif_bodies) = ifthenelse.get_elif_pair_list()
    else_body = ifthenelse.get_else()

    # add if header
    if_idx = mapping.get_if_idx()
    mapping.set_if_idx(if_idx + 1)

    if_header = f"if_header_{if_idx}"
    cmd = (LABEL, if_header)
    cmd_stack.append(cmd)

    # define end if-then-else footer
    if_then_else_footer = f'if_then_else_footer_{if_idx}'

    # negate if guard condition
    if_guard_reg = gen_expr(if_guard, mapping, cmd_stack)
    cmd = (NOT, if_guard_reg, if_guard_reg)
    cmd_stack.append(cmd)

    # add the if guard condition to branch
    if_footer = f"if_footer_{if_idx}"
    cmd = (BEQ, if_guard_reg, ZERO, if_footer)
    cmd_stack.append(cmd)

    # generate body of if loop
    for phrase in if_body:
        gen_phrase(phrase, mapping, cmd_stack)

    # add in absolute branch to if then else footer
    cmd = (BEQ, ZERO, ZERO, if_then_else_footer)
    cmd_stack.append(cmd)

    # add in if footer
    cmd = (LABEL, if_footer)
    cmd_stack.append(cmd)

    for i in range(len(elif_guards)):
        elif_guard = elif_guards[i]
        elif_body = elif_bodies[i]

        # add elif header
        elif_header = f"elif_header_{if_idx}_{i + 1}"
        cmd = (LABEL, elif_header)
        cmd_stack.append(cmd)

        # negate elif guard condition
        elif_guard_reg = gen_expr(elif_guard, mapping, cmd_stack)
        cmd = (NOT, elif_guard_reg, elif_guard_reg)
        cmd_stack.append(cmd)

        # add the elif guard condition to branch
        elif_footer = f"elif_footer_{if_idx}_{i + 1}"
        cmd = (BEQ, elif_guard_reg, ZERO, elif_footer)
        cmd_stack.append(cmd)

        # generate body of elif loop
        for phrase in elif_body:
            gen_phrase(phrase, mapping, cmd_stack)

        # add in absolute branch to if then else footer
        cmd = (BEQ, ZERO, ZERO, if_then_else_footer)
        cmd_stack.append(cmd)

        # add in elif footer:
        cmd = (LABEL, elif_footer)
        cmd_stack.append(cmd)

    # add in else body
    if else_body != None:
        for phrase in else_body:
            gen_phrase(phrase, mapping, cmd_stack)

    # generate if then else footer
    cmd = (LABEL, if_then_else_footer)
    cmd_stack.append(cmd)


def gen_function(_func, mapping, cmd_stack):
    """
    function_header_idx
    function_prologue_idx
    store all variables
    move fp down
    move sp down
    function_body_idx
    function_body
    function_epilogue_idx
    restore all variables
    move fp up
    move sp up

    CALLING CONVENTIONS
    ===============================
    -> Old FP
    Parent Stack Frame


    ===============================
    -> Old SP
    New (Child) Stack Frame
    -----------------------
    -> New FP
    number of args (implicit, not stored in stack or calling conventions)
    Incoming Args (all on stack) [these are done at function application time]
    Saved RA
    Saved FP
    Saved SP
    Saved Regs (all 32 regs that are not RA, FP, SP and ZERO)
    Shift Stack Pointer
    Shift Frame Pointer
    -----------------------
    New (Child) Stack Frame
    ===============================
    -> New SP
    """

    func_assign = _func.get_assign()
    func_name = func_assign.get_name().get_value()
    func_args = list(map(lambda arg: arg.get_value(), func_assign.get_args()))
    func_body = func_assign.get_body()

    # get all variable names
    incoming_vars = func_args
    closure_vars = mapping.get_closure_vars()
    local_func_vars = set(get_all_vars(func_body))
    local_func_vars = local_func_vars.difference(
        incoming_vars)  # remove incoming vars
    new_closure_vars = list(set(closure_vars).union(
        set(incoming_vars).union(local_func_vars)))

    num_vars = len(closure_vars) + len(incoming_vars) + \
        len(local_func_vars) + N_REGISTERS

    new_var_stack_map = {}
    i = 1
    # bottom of stack
    for var_name in local_func_vars:
        new_var_stack_map[var_name] = SIZEOF[INT] * i + \
            SIZEOF[INT] * N_REGISTERS  # relative to SP
        i += 1

    # middle of stack
    for var_name in closure_vars:
        new_var_stack_map[var_name] = SIZEOF[INT] * i + \
            SIZEOF[INT] * N_REGISTERS  # relative to SP
        i += 1

    # top of stack
    for var_name in incoming_vars:
        new_var_stack_map[var_name] = SIZEOF[INT] * i + \
            SIZEOF[INT] * N_REGISTERS  # relative to SP
        i += 1

    # append a new mapping
    mappings_dict = mapping.get_mappings()
    new_reg_var_map = deepcopy(
        mapping.get_reg_var_map())  # hold register state
    new_mapping = Mappings(
        new_reg_var_map, new_var_stack_map, new_closure_vars, closure_vars)
    if func_name not in mappings_dict:
        mappings_dict[func_name] = new_mapping
    mapping.set_mappings(mappings_dict)

    # set current function
    mapping.set_curr_func(func_name)

    ####################### FUNCTION BODY CODE ########################

    # add in function header
    func_header = f"{func_name}_header"
    cmd = (LABEL, func_header)
    cmd_stack.append(cmd)

    # add in function prologue
    func_prologue = f"{func_name}_prologue"
    cmd = (LABEL, func_prologue)
    cmd_stack.append(cmd)

    # save all 32 registers
    for i in range(1, N_REGISTERS + 1):
        reg = ALL_REGISTERS[i - 1]
        save_reg_cmd = (SW, reg, i * SIZEOF[INT], SP)
        cmd_stack.append(save_reg_cmd)

    # shift stack pointer and frame pointer commands
    cmd = (ADDI, SP, SP, -1 * SIZEOF[INT] * (num_vars + 1))
    cmd_stack.append(cmd)

    cmd = (ADDI, FP, FP, SIZEOF[INT] * (num_vars))
    cmd_stack.append(cmd)

    # add in function body
    func_body_label = f"{func_name}_body"
    cmd = (LABEL, func_body_label)
    cmd_stack.append(cmd)

    # add in body
    for phrase in func_body:
        gen_phrase(phrase, mapping, cmd_stack)

    # add in epilogue
    func_epilogue = f"{func_name}_epilogue"
    cmd = (LABEL, func_epilogue)
    cmd_stack.append(cmd)

    # restore all registers
    for i in range(1, N_REGISTERS + 1):
        reg = ALL_REGISTERS[i - 1]
        save_reg_cmd = (LW, reg, i * SIZEOF[INT], SP)
        cmd_stack.append(save_reg_cmd)

    # restore sp
    cmd = (ADDI, SP, SP, 1 * SIZEOF[INT] * (num_vars + 1))
    cmd_stack.append(cmd)

    # jalr to ra
    cmd = (JALR, ZERO, 0, RA)
    cmd_stack.append(cmd)


def gen_return(ret, mapping, cmd_stack):
    """
    gen_return(ret, mapping, cmd_stack) jumps to the function epilogue
    beq x0, x0, {function_name}_epilogue
    """
    function_name = mapping.get_curr_func()
    function_epilogue = f"{function_name}_epilogue"
    cmd = (BEQ, ZERO, ZERO, function_epilogue)
    cmd_stack.append(cmd)
    return


def gen_declare_array(array, mapping, cmd_stack):
    pass


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
    elif type(phrase) == ast_generator_c.IfThenElse:
        return gen_if_then_else(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.DeclareFunc:
        return gen_function(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.Return:
        return gen_return(phrase, mapping, cmd_stack)
    elif type(phrase) == ast_generator_c.DeclareArray:
        return gen_declare_array(phrase, mapping, cmd_stack)


def gen_program(program):
    cmd_stack = []

    cmd = (LABEL, "__main__")
    cmd_stack.append(cmd)

    mapping = Mappings(START_REG_VAR_MAP, [], [], [])

    phrases = program.get_phrases()
    main_function = ast_generator_c.DeclareFunc(None, ast_generator_c.Function(
        ast_generator_c.VarValue('__main__'), [], phrases))

    gen_function(main_function, mapping, cmd_stack)

    cmd = (LABEL, "__start__")
    cmd_stack.append(cmd)

    cmd = (ADDI, SP, SP, START_STACK)
    cmd_stack.append(cmd)

    cmd = (JAL, RA, "__main__")
    cmd_stack.append(cmd)

    return cmd_stack


if __name__ == "__main__":
    program = r"~not False; ~ -3; fun (|int -> int|) int_id x -> return x; endfun ~3 + 4; ~int_id(2); ~3 - 4; int x := 3; x:= 2; int z := 2; z := z + x + x; while True dowhile x := 1; endwhile for i from 1 to 3 by 1 dofor x := 1; endfor if True then int y := 4; endif"
    ir = gen_program(
        type_check_c.type_check(
            ast_generator_c.parse_program(
                lexer_c.lex(program))))
    for triple in ir:
        print(triple)

# TODO: translate to normal form instread of triples
# TODO: Heap
# TODO: Global
# TODO: Data
# TODO: BSS
# TODO: Text
