#!/usr/bin/env python3
# binary_search_tree.py

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

class BinarySearchTreeNode:

	def __init__(self, data):
		"""Initialize all instance variables of node to None."""
		self.left = None
		self.right = None
		self.parent = None
		self.data = data

	def __str__(self):
		"""Print data."""
		return str(self.data)

class BinarySearchTree:
	"""Binary tree properties:
	1. left child key <= parent key
	2. right child key >= parent key
	"""

	def __init__(self, get_key_func=None, nil=None):
		"""Initialize binary search tree.

		Arguments: 
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.
		nil -- sentinel value for the parent of the root and children of the
		leaves of the tree. Optional parameter that is given when implementing
		subclasses of BinarySearchTree. 
		"""
		if get_key_func is None:
			self.get_key = lambda x: x
		else:
			self.get_key = get_key_func

		if nil is None:
			self.nil = BinarySearchTreeNode(None)
		else:
			self.nil = nil 	  # may be RedBlackTreeNode, ...
		self.root = self.nil  # empty tree

	def get_root(self):
		"""Return root."""
		return self.root

	def inorder_tree_walk(self, x, func=print):
		"""Run a function on all the nodes of the subtree rooted at node x in an inorder tree walk.

		Arguments:
		x -- root of the subtree
		func -- function to run on each node in the subtree.  If omitted, print.
		"""
		# Run func on the key of the root in between visiting the left and right subtrees.
		if x != self.nil:
			self.inorder_tree_walk(x.left, func)
			func(x)
			self.inorder_tree_walk(x.right, func)

	def search(self, x, k):
		"""Return a node with a given key k in the subtree rooted at x, or self.nil if no node with key k exists."""
		if x == self.nil or k == self.get_key(x.data):
			return x
		elif k < self.get_key(x.data):
			return self.search(x.left, k)   # if present, k must be in left subtree
		else:
			return self.search(x.right, k)  # if present, k must be in right subtree

	def iterative_search(self, x, k):
		"""Return a node with a given key k in the subtree rooted at x, or self.nil if no node with key k exists."""
		while x != self.nil and k != self.get_key(x.data):
			if k < self.get_key(x.data):
				x = x.left   # if present, k must be in the left subtree
			else:
				x = x.right  # if present, k must be in the right subtree
		return x

	def minimum(self, x):
		"""Return a node in subtree rooted at x with the smallest key."""
		while x.left != self.nil:
			x = x.left  # keep going left
		return x        # leftmost key

	def maximum(self, x):
		"""Return a node in subtree rooted at x with the largest key."""
		while x.right != self.nil:
			x = x.right  # keep going right
		return x         # rightmost key

	def successor(self, x):
		"""Return the node in the subtree rooted at x with the smallest key greater than x's key."""
		if x.right != self.nil:
			return self.minimum(x.right)  # leftmost node in right subtree
		# Find the lowest ancestor of x whose left child is also an ancestor of x.
		y = x.parent
		while y != self.nil and x == y.right:  # continue up the tree
			x = y
			y = y.parent
		return y	

	def predecessor(self, x):
		"""Return the node in the subtree rooted at x with the greatest key less than x's key."""
		if x.left != self.nil:
			return self.maximum(x.left)  # rightmost node in left subtree
		# Find the lowest ancestor of x whose right child is also an ancestor of x.
		y = x.parent
		while y != self.nil and x == y.left:  # continue up the tree
			x = y
			y = y.parent
		return y	

	def tree_insert(self, data):
		"""Initialize a node with data and insert into this binary search tree."""
		z = BinarySearchTreeNode(data)
		# Initialize node's left and right child pointers with defined nil values.
		z.right = self.nil
		z.left = self.nil

		self.tree_insert_node(z)

	# Helper method for inserting a node.  Assumes that node z is already created and initialized.
	def tree_insert_node(self, z):
		"""Insert node z into this binary search tree."""
		x = self.root         # node being compared with z
		y = self.nil          # y will be the parent of z
		while x != self.nil:  # descend until reaching a leaf
			y = x
			if self.get_key(z.data) < self.get_key(x.data):
				x = x.left
			else:
				x = x.right
		z.parent = y  # found the location -- insert z with parent y
		if y == self.nil:
			self.root = z  # tree was empty
		elif self.get_key(z.data) < self.get_key(y.data):
			y.left = z     # assign z as y's left child
		else:
			y.right = z    # assign z as y's right child

	def transplant(self, u, v):
		"""Replace the subtree rooted at node u with the subtree rooted at node v."""
		if u.parent == self.nil:
			self.root = v         # replacing the root
		elif u == u.parent.left:  # is u a left child?
			u.parent.left = v     # update left child to v
		else:                     # u is a right child
			u.parent.right = v    # update right child to v

		# Differ from the textbook because here we have a self.nil value as a node, so
		# that methods can be used for subclasses of BST.  No need to test whether v
		# has a parent--it does, even if v is self.nil.
		v.parent = u.parent       # update v's parent

	def tree_delete(self, z):
		"""Delete node z from this binary search tree and maintain the binary search tree property.

		Assumption:
		Node z appears in this binary search tree.
		"""
		if z is None or z == self.nil:
			raise RuntimeError("Cannot delete sentinel or None node.")

		if z.left == self.nil:
			self.transplant(z, z.right)      # replace z by its right child
		elif z.right == self.nil:
			self.transplant(z, z.left)       # replace z by its left child
		else:
			y = self.minimum(z.right)        # y is z's successor
			if y != z.right:                 # is y farther down the tree?
				self.transplant(y, y.right)  # replace y by its right child
				y.right = z.right            # z's right child becomes y's right child
				y.right.parent = y 	
			self.transplant(z, y)            # replace z by its successor y
			y.left = z.left                  # and give z's left child to y, which had no left child
			y.left.parent = y

	def is_BST(self, x=None):
		"""Return a boolean indicating whether this tree obeys the binary search tree properties.

		Argument:
		x -- root of a subtree.  None indicates root of the entire BST.
		"""
		if x is None:
			x = self.root
		if x == self.nil:
			return True                    # for an empty BST
		if x.left is not self.nil:         # check the left subtree
			if self.get_key(x.left.data) > self.get_key(x.data):
				return False               # left child's key > x's key
			elif not self.is_BST(x.left):  # check the rest of the left subtree
				return False
		if x.right is not self.nil:        # check the right subtree
			if self.get_key(x.right.data) < self.get_key(x.data):
				return False               # right child's key < x's key
			elif not self.is_BST(x.right):
				return False               # check the rest of the right subtree

		return True                        # no error found in the subtree rooted at x

	def pretty_print(self, node, depth=0):
		"""Return a string representing a subtree of a binary search tree with nodes of the same depth in the same column.
		If you tilt your head to the left, it should look like the nodes are positioned correctly.

		Arguments:
		node -- root of a subtree to print
		depth -- depth of the node within the binary search tree
		"""
		result = ""
		if node == self.nil:
			return result
		# Print the right subtree.  Printing right before left so that the BST looks correct with head tilted.
		if node.right != self.nil:
			result += self.pretty_print(node.right, depth + 1)
		result += ('  ' * depth) + str(node) + '\n'  # print this node
		# Print the left subtree.
		if node.left != self.nil:
			result += self.pretty_print(node.left, depth + 1)
		return result

	def __str__(self):
		"""Return a string representing a binary search tree with nodes of the same depth in the same column.
		If you tilt your head to the left, it should look like the nodes are positioned correctly."""
		return self.pretty_print(self.root)


# Testing
if __name__ == "__main__":

	import numpy as np
	from key_object import KeyObject

	# Insert. 
	binary_tree1 = BinarySearchTree()
	array1 = np.arange(0, 100, 13)
	np.random.shuffle(array1)
	for value in array1:
		binary_tree1.tree_insert(value)
	print(binary_tree1.is_BST())
	print(binary_tree1)
	binary_tree1.inorder_tree_walk(binary_tree1.get_root())
	# Search.
	node39 = binary_tree1.search(binary_tree1.get_root(), 39)
	print("Found:", node39)
	# Unsuccessful search. 
	print("Found:", binary_tree1.search(binary_tree1.get_root(), 55))
	# Iterative. 
	print("Found:", binary_tree1.iterative_search(binary_tree1.get_root(), 39))
	print("Found:", binary_tree1.iterative_search(binary_tree1.get_root(), 55))
	# Minimum and maximum. 
	print("Max:", binary_tree1.maximum(binary_tree1.get_root()))
	print("Min:", binary_tree1.minimum(binary_tree1.get_root()))
	# Delete. 
	binary_tree1.tree_delete(node39)
	print("After deleting 39: ")
	print(binary_tree1.is_BST())
	print(binary_tree1)
	binary_tree1.inorder_tree_walk(binary_tree1.get_root(), lambda x: print("Node:", x))
	# Delete node that does not exist.
	node100 = BinarySearchTreeNode(100)
	# try:
	# 	binary_tree1.tree_delete(node100)  # throws error; comment out to avoid error
	# except RuntimeError as e:
	# 	print(e)
	print()

	# Textbook example. 
	binary_tree2 = BinarySearchTree()
	list1 = [15, 18, 6, 3, 2, 4, 7, 13, 9, 17, 20]
	for value in list1:
		binary_tree2.tree_insert(value)
	print(binary_tree2.is_BST())
	print(binary_tree2)
	binary_tree2.inorder_tree_walk(binary_tree2.get_root())
	# Successor and predecessor.
	print("Successor:", binary_tree2.successor(binary_tree2.get_root()))  # should be 17
	print("Predecessor:", binary_tree2.predecessor(binary_tree2.get_root()))  # should be 13
	print("Successor: ", binary_tree2.successor(binary_tree2.search(binary_tree2.get_root(), 13)))  # should be 15
	print("Predecessor:", binary_tree2.predecessor(binary_tree2.search(binary_tree2.get_root(), 7)))  # should be 6

	# Delete the remaining nodes, one by one.
	array2 = np.array(list1)
	np.random.shuffle(array2)
	for value in array2:
		print("After deleting " + str(value) + ":")
		binary_tree2.tree_delete(binary_tree2.search(binary_tree2.get_root(), value))
		print(binary_tree2.is_BST())
		print(binary_tree2)

	# Binary tree of objects. 
	binary_tree3 = BinarySearchTree(KeyObject.get_key)
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	list3 = []
	for i in range(len(states)):
		list3.append(KeyObject(states[i], i))
	array3 = np.array(list3)
	np.random.shuffle(array3)
	for x in array3:
		binary_tree3.tree_insert(x)
	print(binary_tree3.is_BST())
	print(binary_tree3)

	# If get_key not provided, must define __gt__ or __lt__ for objects in the BST.
	binary_tree4 = BinarySearchTree()
	for x in array3:
		binary_tree4.tree_insert(x)
	print(binary_tree4)
	print(binary_tree4.is_BST())

	# Binary tree that does not have the BST property.
	binary_tree5 = BinarySearchTree()
	binary_tree5.tree_insert(100)
	new_node = BinarySearchTreeNode(101)
	new_node.left = binary_tree5.nil
	new_node.right = binary_tree5.nil
	binary_tree5.root.left = new_node
	new_node.parent = binary_tree5.get_root()
	print(binary_tree5.is_BST())
	print(binary_tree5)

	# Large tree. 
	binary_tree6 = BinarySearchTree()
	array2 = np.arange(-1000, 10000, 1000)
	np.random.shuffle(array2)
	for value in array2:
		binary_tree6.tree_insert(value)
	print(binary_tree6.is_BST())
