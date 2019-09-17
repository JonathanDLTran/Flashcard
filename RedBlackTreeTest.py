from RedBlackTree import *


def test_tree():
    print("test tree initialization")
    rb = RedBlackTree(0)
    assert rb.getValue() == 0
    left = RedBlackTree(1)
    left.getValue() == 1
    rb.addLeftTree(left)
    assert left.getParent() == rb
    assert rb.getValue() == 0
    assert rb.leftTree == left
    right = RedBlackTree(-1)
    right.getValue() == -1
    rb.addRightTree(right)
    assert rb.rightTree == right
    assert rb.getValue() == 0
    assert right.getParent() == rb
    right.getValue() == -1
    left.getValue() == 1

    rb = RedBlackTree(10)
    rb.binaryInsert(7)
    assert rb.getLeftTree().getValue() == 7
    rb.binaryInsert(12)
    assert rb.getRightTree().getValue() == 12
    rb.binaryInsert(14)
    assert rb.getRightTree().getRightTree().getValue() == 14
    print("pass tree initialization")


def test_left_rotate():
    print("Test left rotate")
    rb = RedBlackTree(5)
    left = RedBlackTree(3)
    right = RedBlackTree(7)
    rb.addLeftTree(left)
    rb.addRightTree(right)
    left_left = RedBlackTree(2)
    left_right = RedBlackTree(4)
    left.addLeftTree(left_left)
    left.addRightTree(left_right)

    rb.left_rotate()
    assert rb.getParent() == left
    assert rb.getRightTree() == right
    assert rb.getLeftTree() == left_right
    assert rb.getParent().getLeftTree() == left_left
    assert rb.getParent().getParent() == None
    assert rb.getRightTree().getLeftTree() == None
    assert rb.getRightTree().getRightTree() == None
    assert rb.getLeftTree().getRightTree() == None
    assert rb.getLeftTree().getLeftTree() == None
    assert rb.getParent().getLeftTree().getRightTree() == None
    assert rb.getParent().getLeftTree().getLeftTree() == None

    rb1 = RedBlackTree(5)
    right = RedBlackTree(7)
    rb1.addRightTree(right)
    rb1.left_rotate()
    assert rb1.getParent() == None
    assert rb1.getRightTree() == right
    assert rb1.getLeftTree() == None

    parent = RedBlackTree(10)
    parent.binaryInsert(24)
    parent.binaryInsert(3)
    parent.binaryInsert(29)
    parent.binaryInsert(16)
    parent.binaryInsert(12)
    parent.binaryInsert(17)
    other_center = parent.getLeftTree()
    central = parent.getRightTree()
    left = central.getLeftTree()
    right = central.getRightTree()
    left_right = left.getRightTree()
    left_left = left.getLeftTree()
    assert parent.getValue() == 10
    assert other_center.getValue() == 3
    assert central.getValue() == 24
    assert left.getValue() == 16
    assert right.getValue() == 29
    assert left_right.getValue() == 17
    assert left_left.getValue() == 12

    central.left_rotate()
    assert central.getRightTree() == right
    assert central.getLeftTree() == left_right
    assert central.getParent() == left
    assert left.getLeftTree() == left_left
    assert left.getParent() == parent
    assert parent.getRightTree() == left
    assert left.getRightTree() == central
    assert right.getParent() == central
    assert left_right.getParent() == central
    assert left_left.getParent() == left
    assert parent.getParent() == None
    assert parent.getLeftTree() == other_center
    assert other_center.getParent() == parent

    print("pass left rotate")


def test_right_rotate():
    print("Test right rotate")
    print("pass right rotate")


test_tree()
test_left_rotate()
test_right_rotate()
