#!/usr/bin/env python3
# interval_tree.py

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


class Interval:

	def __init__(self, low, high):
		"""Data for an interval node. The interval is closed: [low, high]."""
		self.low = low
		self.high = high

	def overlap(self, other):
		"""Return a boolean indicating whether this interval overlaps another interval."""
		return self.low <= other.high and other.low <= self.high

	@staticmethod
	def get_key(x):
		"""Keyed by the lower bound of interval."""
		return x.low

	def __str__(self):
		"""Return a string of the interval notation."""
		return "[" + str(self.low) + ", " + str(self.high) + "]"


class IntervalTreeNode(RedBlackTreeNode):

	def __init__(self, interval):
		"""Initialize node a with an interval as data """
		RedBlackTreeNode.__init__(self, interval)
		if interval is not None:
			# Maximum value of any interval endpoint stored in the subtree rooted at x.
			self.max = interval.high
		else:
			self.max = float('-inf')  # value in the sentinel, guaranteed to not overlap

	def __str__(self):
		"""Return a string with <interval>: <color>, max = <max>."""
		return RedBlackTreeNode.__str__(self) + ", max = " + str(self.max)


class IntervalTree(RedBlackTree):

	def __init__(self, get_key_func=None):
		"""Initialize this IntervalTree with sentinel that is a IntervalTreeNode.

		Argument: 
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used. 
		"""
		RedBlackTree.__init__(self, get_key_func, IntervalTreeNode(None))

	def left_rotate(self, x):
		"""Call red-black tree left_rotate and fix the max attributes. """
		y = x.right
		RedBlackTree.left_rotate(self, x)

		# Update maxes of the two nodes affected by rotation.
		y.max = x.max
		x.max = max(x.data.high, x.left.max, x.right.max)

	def right_rotate(self, x):
		""" Call red-black tree right_rotate and fix the max attributes. """
		y = x.left
		RedBlackTree.right_rotate(self, x)

		# Update sizes of the two nodes affected by rotation.
		y.max = x.max
		x.max = max(x.data.high, x.left.max, x.right.max)

	def tree_insert(self, interval):
		"""Instantiate a node and insert it into this interval tree."""
		z = IntervalTreeNode(interval)

		# Initialize the node's left and right with defined nil values to
		# maintain proper tree structure.
		z.left = self.nil
		z.right = self.nil

		self.insert_node(z)

	def insert_node(self, z):
		"""Insert node z and update the max attributes of its ancestors."""
		# Update max fields from root down to where node will be inserted.
		i = self.root
		while i != self.nil:
			i.max = max(z.max, i.max)  # update maxes in the path
			# Continue left or right down the path.
			if self.get_key(z.data) < self.get_key(i.data):
				i = i.left
			else:
				i = i.right

		# Insert the node.
		RedBlackTree.insert_node(self, z)

	def tree_delete(self, z):
		"""Delete node z and update the max attributes following parent pointers."""
		has_two_children = False
		z.max = max(z.left.max, z.right.max)  # z's max will not be a contender for max

		if z.left != self.nil and z.right != self.nil:  # does z have two children?
			successor = self.minimum(z.right)
			i = successor.parent  # start at the parent of z's successor
			has_two_children = True
		else:
			i = z.parent  # otherwise, start at the parent of the deleted node.

		# Go up the tree following parent pointers, updating max.
		while i != self.nil:
			i.max = max(i.data.high, i.left.max, i.right.max)
			i = i.parent

		# If the successor replaces z, update the max of the successor before fixing up.
		if has_two_children:
			successor.max = z.max

		RedBlackTree.tree_delete(self, z)

	def interval_search(self, interval):
		"""Search for an interval that overlaps with a given interval. 

		Returns:
		A node that overlaps with given interval or sentinel if not found.
		"""
		x = self.root
		while x != self.nil and not interval.overlap(x.data):
			if x.left != self.nil and x.left.max >= interval.low:
				x = x.left  # overlap in left subtree or no overlap in right subtree
			else:
				x = x.right  # no overlap in left subtree
		return x  # x may be self.nil if not found.

	def is_IntTree(self):
		"""Return a boolean indicating whether this tree maintains interval tree properties."""
		# Must be a valid red black tree.
		if not RedBlackTree.is_rb_tree(self):
			return False

		return self.is_IntTree_helper(self.root) is not None

	def is_IntTree_helper(self, node):
		"""Return the max value in this node's subtree or None if not valid interval tree."""
		if node == self.nil:
			return float('-inf')
		l_max = self.is_IntTree_helper(node.left)
		r_max = self.is_IntTree_helper(node.right)
		# Max should be max of left and right max and its own high end.
		if l_max is None or r_max is None or max(l_max, r_max, node.data.high) != node.max:
			return None
		else:
			return max(l_max, r_max, node.data.high)


# Testing
if __name__ == "__main__":

	import numpy as np

	# Example intervals from textbook.
	intervals = [Interval(0, 3), Interval(5, 8), Interval(6, 10), Interval(8, 9),
				 Interval(15, 23), Interval(16, 21), Interval(17, 19), Interval(19, 20),
				 Interval(25, 30), Interval(26, 26)]
	array1 = np.array(intervals)
	np.random.shuffle(array1)
	int_tree1 = IntervalTree(Interval.get_key)
	for i in intervals:
		int_tree1.tree_insert(i)
	print(int_tree1.is_IntTree())
	print(int_tree1)
	for i in [Interval(-2, -1), Interval(-1, 1), Interval(11, 14),
			  Interval(18, 19), Interval(22, 24), Interval(31, 33)]:
		print(i, int_tree1.interval_search(i))
	print()

	# Insert. 
	int_tree2 = IntervalTree(Interval.get_key)
	array2 = np.arange(1, 200, 13)
	for value in array2:
		int_tree2.tree_insert(Interval(value, value + 1))
	print(int_tree2.is_IntTree())
	print(int_tree2)
	int2 = int_tree2.interval_search(Interval(26, 30))
	print("After deleting interval " + str(int2) + ":")
	int_tree2.tree_delete(int2)
	print(int_tree2.is_IntTree())
	print(int_tree2)
	print(int_tree2.interval_search(Interval(201, 203)))  # unsuccessful interval_search

	# Exhaustive testing. 
	int_tree3 = IntervalTree(Interval.get_key)
	array3 = np.arange(-100, 1000, 2)
	np.random.shuffle(array3)
	for value in array3:
		int_tree3.tree_insert(Interval(value, value + 1))
		if not int_tree3.is_IntTree():
			print("inserting: " + str(Interval(value, value + 1)))
			print(int_tree3)
			break
	print(int_tree3.is_IntTree())
	# Delete everything.
	np.random.shuffle(array3)
	for value in array3:
		to_delete = int_tree3.interval_search(Interval(value, value + 1))
		int_tree3.tree_delete(to_delete)
		if not int_tree3.is_IntTree():
			print("deleting: " + str(Interval(value, value + 1)))
			print(int_tree3)
			break
	print(int_tree3.is_IntTree())
