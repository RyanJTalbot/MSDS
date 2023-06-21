#!/usr/bin/env python3
# order_statistic_tree.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao

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

from red_black_tree import *


class OSTreeNode(RedBlackTreeNode):

	def __init__(self, data):
		"""Initialize a RedBlackTreeNode with an additional size variable."""
		RedBlackTreeNode.__init__(self, data)
		self.size = 1  # number of internal nodes in the subtree rooted at this node

	def __str__(self):
		"""Return a string with <data>: <color>, size: <size>."""
		return RedBlackTreeNode.__str__(self) + ", size: " + str(self.size)		


class OrderStatisticTree(RedBlackTree):

	def __init__(self, get_key_func=None):
		"""Initialize OrderStatisticTree with a sentinel that is an OSTreeNode.

		Argument: 
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used. 
		"""
		RedBlackTree.__init__(self, get_key_func, OSTreeNode(None))
		self.nil.size = 0

	def OS_select(self, x, i):
		"""Select the ith smallest rank in subtree rooted at node x."""
		r = x.left.size + 1  # rank of x within the subtree rooted at x
		if i == r:   # then r is the ith smallest
			return x
		elif i < r:  # ith smallest is no greater than r
			return self.OS_select(x.left, i)
		else:        # ith smallest is no less than r
			return self.OS_select(x.right, i - r)

	def OS_Rank(self, x):
		"""Return the position of node x in the linear order of keys."""
		r = x.left.size + 1  # rank of x within the subtree rooted at x
		y = x  # root of the subtree being examined
		# Add nodes rooted at y's sibling that precede x. 
		while y != self.root:
			if y == y.parent.right:  # if root of a right subtree ...
				r += y.parent.left.size + 1  # ... add in parent and its left subtree
			y = y.parent  # move y toward the root
		return r

	def left_rotate(self, x):
		"""Augment RedBlackTree.left_rotate to update subtree sizes."""
		y = x.right
		RedBlackTree.left_rotate(self, x)

		# Update sizes of two nodes affected by rotation.
		y.size = x.size
		x.size = x.left.size + x.right.size + 1

	def right_rotate(self, x):
		"""Augment RedBlackTree.right_rotate to update subtree sizes."""

		y = x.left
		RedBlackTree.right_rotate(self, x)

		# Update sizes of two nodes affected by rotation.
		y.size = x.size
		x.size = x.left.size + x.right.size + 1

	def tree_insert(self, data):
		"""Insert node z into this OrderStatisticTree and maintain subtree sizes. """
		z = OSTreeNode(data)

		# Initialize node z's left and right with defined nil values to maintain proper tree structure.
		z.right = self.nil
		z.left = self.nil

		# Insert node z and update subtree sizes.
		self.insert_node(z)

	def insert_node(self, z):
		"""Insert node z into this OrderStatisticTree and maintain subtree sizes."""
		# Increment the size for each node on the path from root to the new leaf.
		i = self.root
		while i != self.nil:
			i.size += 1
			if self.get_key(z.data) < self.get_key(i.data):
				i = i.left
			else:
				i = i.right

		# Insert node z into the tree.
		RedBlackTree.insert_node(self, z)

	def tree_delete(self, z):
		"""Delete node z from this OrderStatisticTree and maintain subtree sizes.

		Assumption:
		Node z exists in the tree.
		"""
		# If z has two children. 
		if z.left != self.nil and z.right != self.nil:
			i = self.successor(z)
			i.size = z.size
		else:
			i = z.parent
		# Decrement the size from lowest node that moves, up to the root.
		while i != self.nil:
			i.size -= 1
			i = i.parent

		# Delete node z from tree tree.
		RedBlackTree.tree_delete(self, z)

	def is_OSTree(self):
		"""Return a boolean indicating whether this is a legal OrderStatisticTree."""
		# Must be valid red-black tree.
		if not RedBlackTree.is_rb_tree(self):
			return False

		return self.is_OSTree_helper(self.root) != -1

	def is_OSTree_helper(self, x):
		"""Return size of the subtree rooted at node x node or -1 is x is root of an invalid OSTree."""
		if x == self.nil:
			return 0  # base case
		l_size = self.is_OSTree_helper(x.left)
		r_size = self.is_OSTree_helper(x.right)
		# Size should be sum of left and right size and 1.
		size = l_size + r_size + 1
		if l_size == -1 or r_size == -1 or size != x.size:
			return -1
		else:
			return size


# Testing
if __name__ == "__main__":
	import numpy as np
	from key_object import KeyObject

	# Insert. 
	os_tree1 = OrderStatisticTree()
	array1 = np.arange(0, 100, 13)
	# np.random.shuffle(array1)
	for value in array1:
		os_tree1.tree_insert(value)
	print(os_tree1)
	print(os_tree1.is_OSTree())
	# Search.
	node39 = os_tree1.search(os_tree1.get_root(), 39)
	print("Found: " + str(node39))
	# Unsuccessful search. 
	print("Found: " + str(os_tree1.search(os_tree1.get_root(), 55)))
	# Iterative. 
	print("Found: " 
		+ str(os_tree1.iterative_search(os_tree1.get_root(), 39)))
	print("Found: " 
		+ str(os_tree1.iterative_search(os_tree1.get_root(), 55)))
	# Minimum and maximum. 
	print("Max: " + str(os_tree1.maximum(os_tree1.get_root()))) 
	print("Min: " + str(os_tree1.minimum(os_tree1.get_root()))) 
	# Select. 
	print(os_tree1.OS_select(os_tree1.get_root(), 4))  # should be 39
	# Rank. 
	print(os_tree1.OS_Rank(node39))  # should be 4
	# Delete. 
	node91 = os_tree1.search(os_tree1.get_root(), 91)
	print("After deleting 91: ")
	os_tree1.tree_delete(node91)
	print(os_tree1.is_OSTree())
	print(os_tree1)
	print("After deleting 39: ")
	os_tree1.tree_delete(node39)
	print(os_tree1.is_OSTree())
	print(os_tree1)

	# Exhaustive testing. 
	os_tree2 = OrderStatisticTree()
	array2 = np.arange(-100, 1000)
	np.random.shuffle(array2)
	for value in array2:
		os_tree2.tree_insert(value) 		# insert
		if not os_tree2.is_OSTree():
			print(os_tree2)
			break
	print(os_tree2.is_OSTree())
	np.random.shuffle(array2)
	for value in array2:
		to_delete = os_tree2.search(os_tree2.get_root(), value)
		os_tree2.tree_delete(to_delete) 	# delete
		if not os_tree2.is_OSTree():
			print(os_tree2)
			break
	print(os_tree2.is_OSTree())
	print()

	# Select and rank.
	os_tree3 = OrderStatisticTree()
	for i in range(30):
		os_tree3.tree_insert(np.random.randint(20))
	print(os_tree3)
	print(os_tree3.is_OSTree())
	os_tree3.tree_insert(-1)
	smallest = os_tree3.OS_select(os_tree3.get_root(), 1)
	print(smallest) 		# should be -1
	print(os_tree3.OS_Rank(smallest))  # should be 1
	print()

	# Tree with objects. 
	os_tree4 = OrderStatisticTree(KeyObject.get_key)
	list1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	for i in range(len(list1)):
		os_tree4.tree_insert(KeyObject(list1[i], i))
	print(os_tree4.is_OSTree())
	print(os_tree4)
	nodeCO = os_tree4.OS_select(os_tree4.get_root(), 6)
	os_tree4.tree_delete(nodeCO)
	print("After deleting CO:")
	print(os_tree4.is_OSTree())
	print(os_tree4)
