#!/usr/bin/env python3
# red_black_tree.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao and Tom Cormen

#########################################################################
#                                                                       #
# Copyright 2022 Massachusetts Institute of Technology                  #
#                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining #
# a copy of this software and associated documentation files (the       #
# "Software"), to deal in the Software without restriction, including   #
# without limitation the rights to use, copy, modify, merge, publish,   #
# distribute, sublicense, and/or sell copies of the Software, and to    #
# permit persons to whom the Software is furnished to do so, subject to #
# the following conditions:                                             #
#                                                                       #
# The above copyright notice and this permission notice shall be        #
# included in all copies or substantial portions of the Software.       #
#                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                 #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS   #
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN     #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE      #
# SOFTWARE.                                                             #
#                                                                       #
#########################################################################

from binary_search_tree import *


class RedBlackTreeNode(BinarySearchTreeNode):

	def __init__(self, data):
		"""Initialize this BinarySearchTreeNode and add a color attribute."""
		BinarySearchTreeNode.__init__(self, data)
		self.is_red = True

	def __str__(self):
		"""Return <data>: <color>."""
		return BinarySearchTreeNode.__str__(self) + ": " + ("red" if self.is_red else "black")


class RedBlackTree(BinarySearchTree):
	""" Red-black tree properties:
	Binary search tree tree plus
	1. Every node is either red or black.
	2. The root is black.
	3. Every leaf is black.
	4. If a node is red, then both its children are black.
	5. For each node, all simple paths from the node to descendant leaves
	contain the same number of black nodes.
	"""

	def __init__(self, get_key_func=None, nil=None):
		"""Initialize this RedBlackTree with asentinel that is a RedBlackTreeNode.

		Arguments: 
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.
		nil -- sentinel value for the parent of the root and children of the
		leaves of the tree. Optional parameter that is given when implementing
		subclasses of RedBlackTree. 
		"""
		if nil is None:
			self.nil = RedBlackTreeNode(None)
		else:
			self.nil = nil  # may be IntervalTreeNode, ...
		BinarySearchTree.__init__(self, get_key_func, self.nil)
		self.nil.is_red = False  # the root must be black

	def left_rotate(self, x):
		"""Make the right child of x become the new root of the subtree with a left rotation.

		Assumptions:
		x has a right child. 
		The root's parent is self.nil.
		""" 
		y = x.right
		x.right = y.left            # turn y's left subtree into x's right subtree
		if y.left != self.nil:      # if y's left subtree is not empty ...
			y.left.parent = x       # ... then x becomes the parent of the subtree's root
		y.parent = x.parent         # x's parent becomes y's parent
		if x.parent == self.nil:    # if x was the root ...
			self.root = y           # ... then y becomes the root
		elif x == x.parent.left:    # otherwise, if x was a left child ...
			x.parent.left = y       # ... then y becomes a left child
		else:
			x.parent.right = y      # otherwise, x was a right child, and now y is
		y.left = x                  # make x become y's left child
		x.parent = y

	def right_rotate(self, x):
		"""Make the left child of x become the new root of the subtree with a right rotation.

		Assumptions:
		x has a left child. 
		The root's parent is self.nil.
		"""
		y = x.left
		x.left = y.right            # turn y's right subtree into x's left subtree
		if y.right != self.nil:     # if y's right subtree is not empty ...
			y.right.parent = x      # ... then x becomes the parent of the subtree's root
		y.parent = x.parent         # x's parent becomes y's parent
		if x.parent == self.nil:    # if x was the root ...
			self.root = y           # ... then y becomes the root
		elif x == x.parent.right:   # otherwise, if x was a right child ...
			x.parent.right = y      # ... then y becomes a left child
		else:
			x.parent.left = y       # otherwise, x was a left child, and now y is
		y.right = x                 # make x become y's right child
		x.parent = y

	def tree_insert(self, data):
		"""Insert a new node with data and maintain the red-black tree."""
		self.insert_node(RedBlackTreeNode(data))  # defaults to red

	def insert_node(self, z):
		"""Insert a new node z and maintain the red-black tree."""
		# Initialize z's left and right with defined nil values to maintain proper tree structure.
		z.right = self.nil
		z.left = self.nil

		BinarySearchTree.tree_insert_node(self, z)  # insert z into the tree
		self.rb_insert_fixup(z)   # correct any violations of red-black properties

	def rb_insert_fixup(self, z):
		"""If the red-black properties are violated after node z was inserted, restore them."""
		while z.parent.is_red:                      # two reds in a row
			if z.parent == z.parent.parent.left:    # is z's parent a left child?
				y = z.parent.parent.right           # y is z's uncle
				if y.is_red:
					# Case 1: z's uncle y is red.
					z.parent.is_red = False         # color z's parent black
					y.is_red = False                # color z's uncle black
					z.parent.parent.is_red = True   # color z's grandparent red
					z = z.parent.parent             # continue from z's grandparent
				else:  # z's uncle y is black
					if z == z.parent.right:
						# Case 2: z is a right child
						z = z.parent
						self.left_rotate(z)         # z is now a left child
					# Case 3: z is a left child
					z.parent.is_red = False
					z.parent.parent.is_red = True 
					self.right_rotate(z.parent.parent)  # no consecutive reds
			else:  # z's parent is a right child
				y = z.parent.parent.left            # y is z's uncle
				if y.is_red:
					# Case 1: z's uncle y is red.
					z.parent.is_red = False         # color z's parent black
					y.is_red = False                # color z's uncle black
					z.parent.parent.is_red = True   # color z's grandparent red
					z = z.parent.parent             # continue from z's grandparent
				else:  # z's uncle y is black
					if z == z.parent.left:
						# Case 2: z is a left child
						z = z.parent
						self.right_rotate(z)        # z is now a right child
					# Case 3: z is a right child
					z.parent.is_red = False
					z.parent.parent.is_red = True
					self.left_rotate(z.parent.parent)  # no consecutive reds
		self.root.is_red = False                    # restore the root as black

	# Unlike the textbook, there is no need to modify the implementation of transplant
	# from the BinarySearchTree class.  It already tests whether u.parent == self.nil,
	# and it already assigns v.parent = u.parent unconditionally.

	def tree_delete(self, z):
		"""Delete z and maintain the red-black tree.

		Assumption:
		Node z exists in the tree.
		"""
		if z is None or z == self.nil:
			raise RuntimeError("Cannot delete sentinel or None node.")

		# y is the node either removed from the tree or moved within the tree.
		y = z
		y_original_color = y.is_red
		if z.left == self.nil:           # z has no left child
			x = z.right                  # x will move into y's position
			self.transplant(z, z.right)  # replace z by its right child
		elif z.right == self.nil:        # z has a left child, but no right child
			x = z.left                   # x will move into y's position.
			self.transplant(z, z.left)   # replace z by its left child
		else: 	                         # two children
			y = self.minimum(z.right)    # y is z's successor
			y_original_color = y.is_red
			x = y.right
			if y != z.right:             # is y farther down the tree?
				self.transplant(y, y.right)  # replace y by its right child
				y.right = z.right        # z's right child becomes y's right child
				y.right.parent = y
			else:
				x.parent = y             # in case x is self.nil
			self.transplant(z, y)        # replace z by its successor y
			y.left = z.left              # and give z's left child to y, which had no left child
			y.left.parent = y
			y.is_red = z.is_red          # give y same color as z
		if not y_original_color:
			# If any red-black violations occurred, correct them.
			self.rb_delete_fixup(x)

	def rb_delete_fixup(self, x):
		"""Maintain the red-black properties after deletion.

		Argument:
		x -- the node that moved into the deleted position
		"""
		while x != self.root and not x.is_red:
			# x is "doubly black."
			if x == x.parent.left:              # is x a left child?
				w = x.parent.right              # w is x's sibling
				if w.is_red:
					# Case 1: x's sibling w is red.
					# Because w is red, w's parent--which is x's parent--must be black.
					# Switch the colors of w and x's parent.
					w.is_red = False
					x.parent.is_red = True
					self.left_rotate(x.parent)
					w = x.parent.right          # transform to case 2, 3, or 4
				if not w.left.is_red and not w.right.is_red:
					# Case 2: x's sibling w is black, and both of w's children are black.
					# Remove one black from x and w.
					w.is_red = True
					x = x.parent                # the extra black moves up one level
				else:
					# Case 3: x's sibling w is black, w's left child is red, 
					# and w's right child is black. 
					if not w.right.is_red:
						# Switch the colors of w and its left child w.left.
						w.left.is_red = False
						w.is_red = True
						self.right_rotate(w)
						w = x.parent.right      # transform to case 4
					# Case 4: x's sibling w is black, and w's right child is red.
					# Color changes and a left rotation on x.parent allow the extra black on x to vanish.
					w.is_red = x.parent.is_red
					x.parent.is_red = False
					w.right.is_red = False
					self.left_rotate(x.parent)
					x = self.root               # the loop terminates upon the next condition test
			else:  # x is a right child
				w = x.parent.left               # w is x's sibling
				if w.is_red:
					# Case 1: x's sibling w is red.
					# Because w is red, w's parent--which is x's parent--must be black.
					# Switch the colors of w and x's parent.
					w.is_red = False
					x.parent.is_red = True
					self.right_rotate(x.parent)
					w = x.parent.left           # transform to case 2, 3, or 4
				if not w.right.is_red and not w.left.is_red:
					# Case 2: x's sibling w is black, and both of w's children are black.
					# Remove one black from x and w.
					w.is_red = True
					x = x.parent                # the extra black moves up one level
				else:
					# Case 3: x's sibling w is black, w's left child is red, 
					# and w's right child is black. 
					if not w.left.is_red:
						# Switch the colors of w and its right child w.right.
						w.right.is_red = False
						w.is_red = True
						self.left_rotate(w)
						w = x.parent.left       # transform to case 4
					# Case 4: x's sibling w is black, and w's right child is red.
					# Color changes and a right rotation on x.parent allow the extra black on x to vanish.
					w.is_red = x.parent.is_red
					x.parent.is_red = False
					w.left.is_red = False
					self.right_rotate(x.parent)
					x = self.root               # the loop terminates upon the next condition test
		x.is_red = False                        # ensure that the root is black

	def is_rb_tree(self):
		"""Return a boolean indicating whether the tree is a legal red-black tree."""
		# Return false if not a binary search tree.
		if not BinarySearchTree.is_BST(self):
			return False
		# The root and sentinel should be black.
		if self.root.is_red or self.nil.is_red:
			return False

		return self.is_rb_subtree(self.root) != -1

	def is_rb_subtree(self, x):
		"""Determines whether a subtree of a red-black tree has valid black-heights and no two red nodes in a row.
		   
		Argument:
		x -- root of the subtree

		Returns:
		-1 for invalid red black tree
		black height for valid red black tree
		"""
		if x == self.nil:
			return 0
		if x.is_red and x.parent.is_red:
			return -1  # two red nodes in a row
		left_black_height = self.is_rb_subtree(x.left)
		right_black_height = self.is_rb_subtree(x.right)
		# The black-heights of the left and right subtrees should be equal.
		if left_black_height == -1 or right_black_height == -1 or left_black_height != right_black_height:
			return -1
		else:
			# Increment the black-height if x is black.
			return left_black_height + int(not x.is_red)


# Testing
if __name__ == "__main__":

	import numpy as np
	from key_object import KeyObject

	# Insert. 
	rb_tree1 = RedBlackTree()
	array1 = np.arange(0, 100, 13)
	np.random.shuffle(array1)
	for value in array1:
		rb_tree1.tree_insert(value)
	print(rb_tree1.is_rb_tree())
	print(rb_tree1)
	rb_tree1.inorder_tree_walk(rb_tree1.get_root())
	# Search.
	node39 = rb_tree1.search(rb_tree1.get_root(), 39)
	print("Found: " + str(node39))
	# Unsuccessful search. 
	print("Found: " + str(rb_tree1.search(rb_tree1.get_root(), 55)))
	# Iterative. 
	print("Found: " 
		+ str(rb_tree1.iterative_search(rb_tree1.get_root(), 39)))
	print("Found: " 
		+ str(rb_tree1.iterative_search(rb_tree1.get_root(), 55)))
	# Minimum and maximum. 
	print("Max: " + str(rb_tree1.maximum(rb_tree1.get_root()))) 
	print("Min: " + str(rb_tree1.minimum(rb_tree1.get_root()))) 
	# Delete. 
	rb_tree1.tree_delete(node39)
	print("After deleting 39: ")
	print(rb_tree1.is_rb_tree())
	print(rb_tree1)
	node52 = rb_tree1.search(rb_tree1.get_root(), 52)
	rb_tree1.tree_delete(node52)
	print("After deleting 52: ")
	print(rb_tree1.is_rb_tree())
	print(rb_tree1)

	rb_tree1.inorder_tree_walk(rb_tree1.get_root())
	# Delete a node that does not exist.
	node99 = rb_tree1.search(rb_tree1.get_root(), 99)
	try:
		rb_tree1.tree_delete(node99)
	except RuntimeError as e:
		print(e)
	print(rb_tree1.is_rb_tree())
	print(rb_tree1)

	# Tree with objects. 
	rb_tree2 = RedBlackTree(KeyObject.get_key)
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	list2 = []
	for i in range(len(states)):
		list2.append(KeyObject(states[i], i))
	array2 = np.array(list2)
	np.random.shuffle(array2)
	for x in array2:
		rb_tree2.tree_insert(x)
	print(rb_tree2.is_rb_tree())
	print(rb_tree2)
	nodeCO = rb_tree2.search(rb_tree2.get_root(), 5)
	rb_tree2.tree_delete(nodeCO)
	print("After deleting CO:")
	print(rb_tree2.is_rb_tree())
	print(rb_tree2)
	# Check that is_rb_tree works correctly by making a black node turn red.
	for x in array2:
		# Find a non-root black node.
		node = rb_tree2.search(rb_tree2.get_root(), KeyObject.get_key(x))
		if not node.is_red and node != rb_tree2.get_root():
			break
	node.is_red = True
	print(rb_tree2.is_rb_tree())
	# Restore blackness to that node, but make two reds in a row.
	node.is_red = False
	for x in array2:
		node = rb_tree2.search(rb_tree2.get_root(), KeyObject.get_key(x))
		if node.is_red:
			break
	node.parent.is_red = True
	print(rb_tree2.is_rb_tree())
	# Restore blackness, but make the root red.
	node.parent.is_red = False
	rb_tree2.get_root().is_red = True
	print(rb_tree2.is_rb_tree())
	# Make the root black but the sentinel red.
	rb_tree2.get_root().is_red = False
	rb_tree2.nil.is_red = True
	print(rb_tree2.is_rb_tree())

	# Exhaustive testing.
	rb_tree3 = RedBlackTree()
	array2 = np.arange(-100, 1000)
	np.random.shuffle(array2)
	for value in array2:
		rb_tree3.tree_insert(value)  # Covers every insert fixup case.
		if not rb_tree3.is_rb_tree():
			print(rb_tree3)
			break
	print(rb_tree3.is_rb_tree())

	np.random.shuffle(array2)
	for value in array2:
		to_delete = rb_tree3.search(rb_tree3.get_root(), value)
		rb_tree3.tree_delete(to_delete)
		if not rb_tree3.is_rb_tree():
			print(rb_tree3)
			break
	print(rb_tree3.is_rb_tree())
