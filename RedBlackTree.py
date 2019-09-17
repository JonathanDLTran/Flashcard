from Constants import *
import Flashcard


class RedBlackTree:
    """
    Color Invariant: Color: Black is True, Red is False
    Class Invariant: The top node of every red back tree is always black,
    moreover, there are never two white nodes in a row. Finally, the number
    of black nodes from the root to ANY leaf is always the same
    """

    def getValue(self):
        """
        Gets value at the current tree [self]'s node
        """
        return self.nodeValue

    def getRightTree(self):
        """
        Gets the right tree of the current tree [self]
        """
        return self.rightTree

    def getLeftTree(self):
        """
        Get the left tree of the current tree [self]
        """
        return self.leftTree

    def getColor(self):
        """
        Gets nodeColor and returns the color
        """
        return self.nodeColor

    def setColor(self, color):
        """
        sets nodeColor to color,
        [bool] color is true if black, false if white
        """
        assert (type(color) == bool)
        self.nodeColor = color

    def getParent(self):
        """
        Returns the parent tree for the given redblacktree [self]
        Requires: [self] is not None
        Raises; assertionError if self is a None object
        """
        assert self != None
        return self.parentTree

    def setParent(self, parent):
        """
        Sets parentTree to parent for the current tree
        Requires: [parent] is a RedBlackTree or parent == None
        Raises: AssertionError if parent is not a RedBlackTree or if parent is not None
        """
        assert isinstance(parent, RedBlackTree) or parent == None
        self.parentTree = parent

    def getCardList(self):
        """
        Gets the cardList stored at the tree root node
        """
        return self.cardList

    def appendCardList(self, card):
        """
        Appends card to the cardlist at the current tree [self] root node
        Raises: AssertionError if card is not a [Flashcard Card]
        """
        assert (type(card) == Flashcard.Card)
        if card not in self.cardList:
            self.cardList.append(card)

    def deleteCard(self, card):
        """
        Removes card from the cardlist at the current tree [self] root node
        Raises: AssertionError if card is not a [Flashcard Card]
        """
        assert type(card) == Flashcard.Card
        if card in self.cardList:
            self.cardList.remove(card)

    def __init__(self, value, color=True, parent=None, left=None, right=None):
        """
        Constructs a new red black tree with [nodevalue] having [value] and
        [leftTree] and [rightTree] being [left] and [right]
        [Color] is assigned [black = True] automatically
        [leftTree] is a red black tree
        [rightTree] is a red black tree
        [parentTree] is the root tree for the current subtree [self] (e.g. parent.right is self, and self.parentTree is parent)
        [cardList] is a list of the cards from which the values come from
            Invariant: values List is always greater than equal 1 in length given there is a non None node
            TODO: this will be implemented in the final red black tree for arbitray search/delete for many cards
         Raises: AssertionError if [left] or [right] is not a [RedBlackTree] or None
                AssertionError if [parentTree] is not a [RedBlackTree] or None
                AssertionError if [color] is not [bool]
        """
        assert (isinstance(parent, RedBlackTree) or parent == None)
        assert (isinstance(left, RedBlackTree) or left == None)
        assert (isinstance(right, RedBlackTree) or right == None)
        assert (type(color) == bool)
        self.nodeValue = value
        self.parentTree = parent
        self.leftTree = left
        self.rightTree = right
        self.nodeColor = color
        self.cardList = []

    def addLeftTree(self, left):
        """
        Appends a [RedBlackTree] [left] to the given tree [self], on the left
        hand side
        Requires: [self] is non Null, so it is actually a [RedBlackTree] object
        Raises: AssertionError if [left] is not a [RedBlackTree] or if left is not None
        """
        assert (isinstance(left, RedBlackTree)) or left == None
        self.leftTree = left
        left.setParent(self)

    def addRightTree(self, right):
        """
        Appends a [RedBlackTree] [right] to the given tree [self], on the right
        hand side
        Requires: [self] is non Null, so it is actually a [RedBlackTree] object
        Raises: AssertionError if [right] is not a [RedBlackTree] or if right is not None
        """
        assert isinstance(right, RedBlackTree) or right == None
        right.setParent(self)
        self.rightTree = right

    def binaryInsert(self, value):
        """
        Inserts value into [self], the red black tree, following the binary tree
        invariants, recursively
        Returns: Tagged Union of where the value comes from: if added to right subtree, then tag (RIGHT, newRB)
            else tag (LEFT, newRB)
        Requires: self is non empty [redblacktree]
        """
        topValue = self.nodeValue
        if value < topValue:
            leftTree = self.getLeftTree()
            if leftTree == None:
                newRB = RedBlackTree(value)
                self.addLeftTree(newRB)
                return (LEFT, newRB)
            else:
                leftTree.binaryInsert(value)
        else:
            rightTree = self.getRightTree()
            if rightTree == None:
                newRB = RedBlackTree(value)
                self.addRightTree(newRB)
                return (RIGHT, newRB)
            else:
                rightTree.binaryInsert(value)

    def redBlackInsert(self, value):
        # TODO : implement algorithm
        node = self.binaryInsert(value)
        direction = node[0]
        tree = node[1]
        if tree.parentTree.getColor() == False:  # case 1
            tree.setColor(True)
            return

        if direction == LEFT:  # add on left, then need to rotate
            tree.setColor(False)
            tree.parentTree.setColor(True)
            self.right_rotate(tree.parentTree)
        # now step 2 of algorithm

        # make sure that you add the right color to the bottom of the tree
        # 0 : if add to right, good, else, rotate the offending node upwards, and switch colors

        # 1 : if black note then add on a white node
        # 2 : if end in a white node, then add on a black node, then rotate the white node up to the black node, and the black node down
            # check if there are double white lines, and fix
            # the fix is: change the first offending white to a black node
            # on the second white node, rotate that white node upwards
            # if no double whites any more, stop
            # if no more rotations able to be done, change the uppermost white node to black. The tree is balanced

    def redBlackDelete(self, value):
        pass

    def determineChild(self, child):
        """
        True if child is the right tree of self, False if child is the left tree of self
        Requires: Child is one of either the left or right subtrees of self
        Requires: Self and Child are not None, and self is a parent node of child
        """
        assert isinstance(child, RedBlackTree)
        return self.getRightTree() == child

    def left_rotate(self):
        # TODO: the singular cases
        """
        Performs a left rotation around the root of self
        Requires: self is not None and is redblacktree
        """
        parent = self.getParent()
        right = self.getRightTree()
        left = self.getLeftTree()

        if left == None:  # case where left is None, cannot rotate into root
            return

        left_right = left.getRightTree()

        if parent != None:  # case where parent is not None, no need to deal with parent
            direction = parent.determineChild(self)
            if direction:
                parent.addRightTree(left)
            else:
                parent.addLeftTree(left)
        elif parent == None:
            left.setParent(None)
        left.addRightTree(self)
        self.addRightTree(right)
        self.addLeftTree(left_right)

    def right_rotate(self):
        """
        Performs a right rotation around root node of self
        Requires: self is not None and is a RedBlacktree
        """
        parent = self.getParent()
        right = self.getRightTree()
        left = self.getLeftTree()

        if right == None:  # case where right is None, cannot rotate into root
            return

        right_left = right.getLeftTree()

        if parent != None:  # case where parent is not None, no need to deal with parent
            direction = parent.determineChild(self)
            if direction:
                parent.addRightTree(right)
            else:
                parent.addLeftTree(right)
        elif parent == None:
            right.setParent(None)
        right.addLeftTree(self)
        self.addRightTree(right_left)
        self.addLeftTree(left)
