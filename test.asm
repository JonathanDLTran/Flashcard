.globl
.data
.text
__main__:
__main___header:
__main___prologue:
	sw x0 4(x2)
	sw x1 8(x2)
	sw x2 12(x2)
	sw x3 16(x2)
	sw x4 20(x2)
	sw x5 24(x2)
	sw x6 28(x2)
	sw x7 32(x2)
	sw x8 36(x2)
	sw x9 40(x2)
	sw x10 44(x2)
	sw x11 48(x2)
	sw x12 52(x2)
	sw x13 56(x2)
	sw x14 60(x2)
	sw x15 64(x2)
	sw x16 68(x2)
	sw x17 72(x2)
	sw x18 76(x2)
	sw x19 80(x2)
	sw x20 84(x2)
	sw x21 88(x2)
	sw x22 92(x2)
	sw x23 96(x2)
	sw x24 100(x2)
	sw x25 104(x2)
	sw x26 108(x2)
	sw x27 112(x2)
	sw x28 116(x2)
	sw x29 120(x2)
	sw x30 124(x2)
	sw x31 128(x2)
	addi x2 x2(-152)
	addi x8 x8(148)
__main___body:
	li x17 222
	li x10 40
	li x11 0
	li x12 0
	li x13 0
	li x14 0
	li x15 0
	ecall
	li x31 3
	sw x31 0(x10)
	li x31 0
	not x31 x31
	andi x31 x31(1)
	li x31 3
	sub x31 x0(x31)
int_id_header:
int_id_prologue:
	sw x0 4(x2)
	sw x1 8(x2)
	sw x2 12(x2)
	sw x3 16(x2)
	sw x4 20(x2)
	sw x5 24(x2)
	sw x6 28(x2)
	sw x7 32(x2)
	sw x8 36(x2)
	sw x9 40(x2)
	sw x10 44(x2)
	sw x11 48(x2)
	sw x12 52(x2)
	sw x13 56(x2)
	sw x14 60(x2)
	sw x15 64(x2)
	sw x16 68(x2)
	sw x17 72(x2)
	sw x18 76(x2)
	sw x19 80(x2)
	sw x20 84(x2)
	sw x21 88(x2)
	sw x22 92(x2)
	sw x23 96(x2)
	sw x24 100(x2)
	sw x25 104(x2)
	sw x26 108(x2)
	sw x27 112(x2)
	sw x28 116(x2)
	sw x29 120(x2)
	sw x30 124(x2)
	sw x31 128(x2)
	addi x2 x2(-136)
	addi x8 x8(132)
int_id_body:
	beq x0 x0(int_id_epilogue)
int_id_epilogue:
	lw x0 4(x2)
	lw x1 8(x2)
	lw x2 12(x2)
	lw x3 16(x2)
	lw x4 20(x2)
	lw x5 24(x2)
	lw x6 28(x2)
	lw x7 32(x2)
	lw x8 36(x2)
	lw x9 40(x2)
	lw x10 44(x2)
	lw x11 48(x2)
	lw x12 52(x2)
	lw x13 56(x2)
	lw x14 60(x2)
	lw x15 64(x2)
	lw x16 68(x2)
	lw x17 72(x2)
	lw x18 76(x2)
	lw x19 80(x2)
	lw x20 84(x2)
	lw x21 88(x2)
	lw x22 92(x2)
	lw x23 96(x2)
	lw x24 100(x2)
	lw x25 104(x2)
	lw x26 108(x2)
	lw x27 112(x2)
	lw x28 116(x2)
	lw x29 120(x2)
	lw x30 124(x2)
	lw x31 128(x2)
	addi x2 x2(136)
	jalr x0 0(x1)
	li x31 3
	add x30 x31(x0)
	li x31 4
	add x30 x30(x31)
	mv x31 x30
	li x31 2
	sw x31 0(x2)
	jal x1 int_id_header
	li x31 3
	add x30 x31(x0)
	li x31 4
	sub x30 x30(x31)
	mv x31 x30
	li x31 3
	add x5 x31(x0)
	li x31 2
	add x5 x31(x0)
	li x31 2
	add x5 x31(x0)
	add x30 x5(x0)
	add x30 x30(x5)
	mv x31 x30
	add x30 x31(x0)
	add x30 x30(x5)
	mv x31 x30
	add x5 x31(x0)
while_header_1:
	li x31 1
	not x31 x31
	beq x31 x0(while_footer_1)
	li x31 1
	add x5 x31(x0)
	beq x0 x0(while_header_1)
while_footer_1:
	li x5 1
for_header_1:
	add x31 x5(x0)
	li x30 3
	bge x31 x30(for_footer_1)
	li x31 1
	add x5 x31(x0)
	addi x5 x5(1)
	beq x0 x0(for_header_1)
for_footer_1:
if_header_1:
	li x31 1
	not x31 x31
	beq x31 x0(if_footer_1)
	li x31 4
	add x5 x31(x0)
	beq x0 x0(if_then_else_footer_1)
if_footer_1:
if_then_else_footer_1:
__main___epilogue:
	lw x0 4(x2)
	lw x1 8(x2)
	lw x2 12(x2)
	lw x3 16(x2)
	lw x4 20(x2)
	lw x5 24(x2)
	lw x6 28(x2)
	lw x7 32(x2)
	lw x8 36(x2)
	lw x9 40(x2)
	lw x10 44(x2)
	lw x11 48(x2)
	lw x12 52(x2)
	lw x13 56(x2)
	lw x14 60(x2)
	lw x15 64(x2)
	lw x16 68(x2)
	lw x17 72(x2)
	lw x18 76(x2)
	lw x19 80(x2)
	lw x20 84(x2)
	lw x21 88(x2)
	lw x22 92(x2)
	lw x23 96(x2)
	lw x24 100(x2)
	lw x25 104(x2)
	lw x26 108(x2)
	lw x27 112(x2)
	lw x28 116(x2)
	lw x29 120(x2)
	lw x30 124(x2)
	lw x31 128(x2)
	addi x2 x2(152)
	jalr x0 0(x1)
__start__:
	addi x2 x2(1879048192)
	jal x1 __main__
