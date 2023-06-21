#!/usr/bin/env python3
# b_tree.py

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

class BTreeNode:

	def __init__(self, n, max_keys, leaf):
		"""Initialize a node of B-tree with number of keys and a boolean indicating whether it is a leaf.

		Arguments:
		n -- number of keys currently stored
		leaf -- True if the node is a leaf, False if not
		"""
		self.n = n          # number of keys currently stored
		self.leaf = leaf    # boolean if node is a leaf
		self.key = [None] * max_keys 	# the keys themselves
		if not leaf:
			self.c = [None] * (max_keys + 1)  # internal nodes store pointers to children

	def disk_read(self):
		"""Placeholder for code to read in the disk block containing this node."""
		pass

	def disk_write(self):
		"""Placeholder for code to write out the disk block containing this node."""
		pass

	def free(self):
		"""Placeholder for code to free the record of this node."""
		pass

	def search(self, k):
		"""Search for a node with a given key k in the subtree rooted at this node.

		Returns:
		Tuple consisting of a node and index such that node.key[index] = k
		"""
		# Find smallest index i such that k <= x.k[i] or else set i to x.n + 1.
		i = 0
		while i < self.n and k > self.key[i]:
			i += 1
		# Have we discovered key k?
		if i < self.n and k == self.key[i]:
			return self, i
		# Either terminate the search unsuccessfully or recursively search a subtree.
		elif self.leaf:
			return None
		else:
			self.c[i].disk_read()
			return self.c[i].search(k)

	def find_greatest_in_subtree(self):
		"""Find the greatest key in the subtree rooted at this node."""
		if self.leaf:
			return self.key[self.n - 1]  # return greatest key
		else:
			# Find the greatest key in the subtree of the greatest child.
			self.c[self.n].disk_read()
			return self.c[self.n].find_greatest_in_subtree()

	def find_smallest_in_subtree(self):
		"""Find the smallest key in the subtree rooted at this node."""
		if self.leaf:
			return self.key[0]  # return smallest key
		else:
			# Find the smallest key in the subtree of the smallest child.
			self.c[self.n].disk_read()
			return self.c[0].find_smallest_in_subtree()

	def shift_left(self, i):
		"""Shift one position to the left keys and children, if this node has children.
		Used for delete. 

		Argument:
		i -- index of where to shift the first element
		"""
		self.key[i: self.n] = self.key[i + 1: self.n] + [None]
		if not self.leaf:
			self.c[i: self.n] = self.c[i + 1: self.n + 1]

		self.n -= 1

	def shift_right(self, i):
		"""Shift one position to the right keys and children, if this node has children.
		Used for delete.

		Argument:
		i -- index of where to shift first element
		"""
		self.key[i:] = [None] + self.key[i: -1]
		if not self.leaf:
			self.c[i:] = [None] + self.c[i: -1]

		self.n += 1

	def __str__(self):
		"""Return a string containing the list of keys."""
		return str(self.key[: self.n])


class BTree:

	def __init__(self, t):
		"""Create an empty root node, based on B_Tree_Create."""
		self.t = t 					# minimum degree of the B-tree
		self.max_keys = 2 * t - 1 	# maximum degree of the B-tree
		self.root = BTreeNode(0, self.max_keys, True)
		self.root.disk_write()

	def search(self, k):
		"""Search for a node with key k starting at the root.

		Returns:
		Tuple consisting of a node and index such that node.key[index] = k
		"""
		return self.root.search(k)

	def split_child(self, x, i):
		"""Split node x.c[i], which is a full child of its parent, which
		is a non-full internal node. Split the node in two and adjust the
		parent so that it has an additional child.

		Arguments:
		x -- parent of the node to split
		i -- this node is c[i] of x
		"""
		y = x.c[i]  # full node to split
		z = BTreeNode(self.t - 1, self.max_keys, y.leaf)  # z will take half of y
		z.key[: self.t - 1] = y.key[self.t: 2 * self.t - 1]  # z gets y's greatest keys

		if not y.leaf:
			z.c[: self.t] = y.c[self.t: 2 * self.t]  # z gets y's corresponding children

		y.n = self.t - 1  # y keeps t-1 keys

		x.c[i + 2: x.n + 2] = x.c[i + 1: x.n + 1]  # shift x's children to the right ...
		x.c[i + 1] = z  # ... to make room for z as a child

		x.key[i + 1: x.n + 1] = x.key[i: x.n]  # shift the corresponding keys in x
		x.key[i] = y.key[self.t - 1]  # insert y's median k

		x.n += 1  # x has gained a child

		y.disk_write()
		z.disk_write()
		x.disk_write()

	def insert(self, k):
		"""Insert key k into this B-tree."""
		r = self.root
		if r.n == self.max_keys:
			s = self.split_root()
			self.insert_nonfull(s, k)
		else:
			self.insert_nonfull(r, k)

	def split_root(self):
		"""Split the root of this B-tree."""
		s = BTreeNode(0, self.max_keys, False)  # s will be the new root
		s.c[0] = self.root
		self.root = s
		self.split_child(s, 0)
		return s

	def insert_nonfull(self, x, k):
		"""Insert key k into non-full node x."""
		i = x.n - 1  # index of last element
		if x.leaf:  # inserting into a leaf?
			while i >= 0 and k < x.key[i]:  # shift keys in x to make room for the key
				x.key[i + 1] = x.key[i]
				i -= 1
			# i may be -1 or key[i] is the rightmost key <= k.
			x.key[i + 1] = k  # insert key k in x
			x.n += 1  # now x has one more key
			x.disk_write()
		else:
			while i >= 0 and k < x.key[i]:  # find the child where key k belongs
				i -= 1
			i += 1
			x.c[i].disk_read()
			if x.c[i].n == self.max_keys:  # split the child if it's full
				self.split_child(x, i)
				if k > x.key[i]:  # does key k go into child i or child i+1?
					i += 1
			self.insert_nonfull(x.c[i], k)

	def delete(self, k):
		"""Delete key k from the B-tree."""
		self.delete_from_subtree(self.root, k)

		# Update root when root is an internal node with no keys.
		if not self.root.leaf and self.root.n == 0:
			self.root = self.root.c[0]

	def delete_from_subtree(self, x, k):
		"""Delete key k from the subtree rooted at node x."""
		if x.leaf:
			# Delete key k from x, if present.
			self.delete_from_leaf(x, k)
		else:  # x is an internal node
			# Search for key k.
			i = 0
			while i < x.n and x.key[i] < k:
				i += 1
			if i < x.n and x.key[i] == k:  # key k is in x.key[i]
				self.delete_from_internal_node(x, i)
			else:
				# If key k is in the subtree, it's in the subtree rooted at child x.c[i].
				child = x.c[i]
				child.disk_read()
				self.ensure_full_enough(x, i)
				self.delete_from_subtree(child, k)

	@staticmethod
	def delete_from_leaf(x, k):
		""" Case 1: Delete key k from node x which is a leaf.
		Do nothing if node x does not contain key k.
		"""
		# Search for key k.
		i = 0
		while i < x.n and x.key[i] < k:
			i += 1
		if i < x.n and x.key[i] == k:
			# Key k is in position i, so shift all keys greater than
			# x.key[i] one position to the left.
			x.shift_left(i)
		x.disk_write()

	def delete_from_internal_node(self, x, i):
		"""Case 2: Delete key k = x.key[i] from internal node x.

		Arguments:
		x -- node
		i -- k = x.key[i] is deleted from node x
		"""
		y = x.c[i]  # child preceding key k
		y.disk_read()
		if y.n >= self.t:
			# Case 2a: y (= x.c[i]) has at least t keys.
			k_prime = y.find_greatest_in_subtree()  # find the predecessor k' of key k in the subtree rooted at y
			y.disk_read()  # because descending through y's subtree might have evicted y from memory
			self.delete_from_subtree(y, k_prime)  # recursively delete key k'
			x.disk_read()  # because deleting key k' might have evicted x from memory
			x.key[i] = k_prime  # replace key k by k'
			x.disk_write()
		else:  # y has fewer than t keys
			z = x.c[i + 1]
			z.disk_read()
			# Symmetrically, examine the child z that follows key k in node x.
			if z.n >= self.t:
				# Case 2b: z (= x.c[i+1]) has at least t keys.  Symmetric to case 2a.
				k_prime = z.find_smallest_in_subtree()  # find the successor key k' of k in the subtree rooted at z
				z.disk_read()  # because descending through z's subtree might have evicted z from memory
				self.delete_from_subtree(z, k_prime)  # recursively delete key k'
				x.disk_read()  # because deleting key k' might have evicted x from memory
				x.key[i] = k_prime  # replace key k by k'
				x.disk_write()
			else:
				# Case 2c: Both y and z have t-1 keys.
				# Merge key k and all of z into y, so that x loses both k and the pointer to z.
				# y then contains 2t-1 keys.  Free z and recursively delete key k from y.
				k = x.key[i]
				y.key[y.n] = k  # merge key k into y
				y.key[y.n + 1: y.n + z.n + 1] = z.key[: z.n]  # merge z into y

				# If y and z are not leaves, copy z's child pointers. 
				if not y.leaf:
					y.c[y.n + 1: y.n + z.n + 2] = z.c[: z.n + 1]
				y.n += z.n + 1 	# update count

				# Remove k and z from this node.
				x.key[i: x.n] = x.key[i + 1: x.n] + [None]
				x.c[i + 1: x.n + 1] = x.c[i + 2: x.n + 1] + [None]
				x.n -= 1

				x.disk_write()
				y.disk_write()
				z.free()

				self.delete_from_subtree(y, k)  # recursively delete key k from y

	def ensure_full_enough(self, x, i):
		"""Ensure that a given child of a node has at least t keys.

		Arguments:
		x -- the node
		i -- ensure that the ith child of node x has at least t keys
		"""
		child = x.c[i]
		if child.n >= self.t:
			return

		# Assign left_sibling, and left_n: the number of keys in the
		# left_sibling. May be None and 0 if does not have a left sibling.
		if i > 0:
			left_sibling = x.c[i - 1]
			left_sibling.disk_read()
			left_n = left_sibling.n
		else:
			left_sibling = None
			left_n = 0

		if left_n >= self.t:
			# Case 3a: x's left sibling has at least t keys.
			# Move a key from x into child, move a key from left_sibling up into x,
			# and move a child pointer from left_sibling into child.
			child.shift_right(0)  # make room

			# Move a key down from node x into child and from left sibling into node x.
			child.key[0] = x.key[i - 1]  # move a key from x into child
			x.key[i - 1] = left_sibling.key[left_n - 1]  # move a key from left_sibling up into x
			left_sibling.key[left_n - 1] = None

			if not child.leaf:
				# Move appropriate child pointer from left_sibling into child.
				child.c[0] = left_sibling.c[left_n]
				left_sibling.c[left_n] = None

			left_sibling.n -= 1

			x.disk_write()
			child.disk_write()
			left_sibling.disk_write()
		else:  # symmetric with right sibling
			if i < x.n:
				# Assign right_sibling, and right_n: the number of keys in the
				# right_sibling. May be None and 0 if does not have right sibling.
				right_sibling = x.c[i + 1]
				right_sibling.disk_read()
				right_n = right_sibling.n
			else:
				right_sibling = None
				right_n = 0

			if right_n >= self.t:  # right sibling has at least t keys
				# Case 3a: x's right sibling has at least t keys.
				# Move a key from x into child, move a key from right_sibling up into x,
				# and move a child pointer from right_sibling into child.
				child.key[child.n] = x.key[i]  # move a key from x into child
				x.key[i] = right_sibling.key[0]  # move a key from right_sibling up into x

				if not child.leaf:
					# Move appropriate child pointer from right_sibling into child.
					child.c[child.n + 1] = right_sibling.c[0]

				# Move all the right sibling's keys and child pointers to the left by one position.
				right_sibling.shift_left(0)
				child.n += 1

				x.disk_write()
				child.disk_write()
				right_sibling.disk_write()
			else:
				# Case 3b: The child and each of its immediate siblings have t - 1 keys.
				# Merge the child with one sibling, including moving a key from x down
				# into the new merged node as the median key of the merged node.
				if left_n > 0:
					# The child has a left sibling.  Merge the child with the left sibling.

					# Move everything in child right by t positions.
					child.key[self.t: self.t + child.n] = child.key[: child.n]
					if not child.leaf:
						child.c[self.t: self.t + child.n + 1] = child.c[: child.n + 1]

					# Take everything from left_sibling.
					child.key[: left_n] = left_sibling.key[: left_n]
					if not child.leaf:
						child.c[: left_n + 1] = left_sibling.c[: left_n + 1]

					# Move a k down from node x into child.
					child.key[self.t - 1] = x.key[i - 1]
					child.n += left_n + 1

					# Since node x is losing key i - 1 and child pointer i - 1,
					# move keys i to n - 1 and children i to n left by one position in this node.
					x.shift_left(i - 1)

					left_sibling.free()
					x.disk_write()
					child.disk_write()
				else:
					# Still in case 3b, but the child has no left sibling.
					# Merge the child with the right sibling.

					# Take everything from right_sibling.
					child.key[child.n + 1: right_n + child.n + 1] = right_sibling.key[: right_n]
					if not child.leaf:
						child.c[child.n + 1: right_n + child.n + 2] = right_sibling.c[: right_n + 1]

					# Move a key down from node x into the child.
					child.key[self.t - 1] = x.key[i]
					child.n += right_n + 1

					# Since node x is losing key i and child pointer i,
					# move keys i + 1 to n - 1 and children i + 2 to n left by one position in this node.
					x.key[i: x.n] = x.key[i + 1: x.n] + [None]
					if not x.leaf:
						x.c[i + 1: x.n] = x.c[i + 2: x.n + 1]

					x.n -= 1

					right_sibling.free()
					x.disk_write()
					child.disk_write()

	def pretty_print(self, node, depth=0):
		"""Return a string of this B-tree's keys with indentation indicating depth.
		Nodes are printed in preorder, from left to right,
		with the keys within each node printed."""
		result = ""
		if node is None:
			return result
		for i in range(depth):		# indent correct amount
			result += "  "
		result += str(node) + "\n"  # append the keys of this node
		if not node.leaf:  # append this node's children, if any
			for i in range(0, node.n+1):
				result += self.pretty_print(node.c[i], depth + 1)
		return result

	def __str__(self):
		"""Print tree from root."""
		return self.pretty_print(self.root)

	def is_btree(self):
		"""Return True if B-tree adheres to the key properties where
		k1 <= x.key[i] <= k2 <= x.key[2] <= ... <= x.key[x.n] <= k(x.n+1).
		Return False otherwise.
		"""
		return self.check_leaf_depths() and self.is_btree_helper(self.root)

	def check_leaf_depths(self):
		"""Return True if all leaves have the same depth, False otherwise."""
		# First determine the depth of the leftmost leaf.
		target_depth = 0
		node = self.root
		while not node.leaf:
			target_depth += 1
			node = node.c[0]  # go to leftmost child

		# Now check all leaves.
		node = self.root
		node_depth = 0
		return self.check_leaf_depths_helper(node, node_depth, target_depth)

	def check_leaf_depths_helper(self, node, node_depth, target_depth):
		"""Return True if all leaves in the subtree rooted at a node have depths
		equal to target_depth."""
		if node.leaf:
			return node_depth == target_depth
		else:  # recurse into the subtree rooted at this node
			node_depth += 1
			for i in range(node.n):
				if not self.check_leaf_depths_helper(node.c[i], node_depth, target_depth):
					return False  # some leaf has the wrong depth
			return True  # leaves in all subtrees are OK

	def is_btree_helper(self, node):
		"""Helper function to determine if the subtree rooted at a node has some properties of B-trees."""
		# This node must have between t-1 and 2t-1 keys.
		if node != self.root:
			if not self.t - 1 <= node.n <= 2 * self.t - 1:
				return False

		# Leaf keys must be sorted.
		if node.leaf:
			for i in range(node.n - 1):
				if node.key[i] >= node.key[i + 1]:
					return False
			return True
			
		# This node is not a leaf.  Each key and child key must be in correct order.
		for i in range(node.n):
			for j in range(node.c[i].n):
				if node.c[i].key[j] >= node.key[i]:
					return False
			# The last key should be less than the keys in the last child.
			for j in range(node.c[node.n].n):
				if node.c[node.n].key[j] <= node.key[node.n - 1]:
					return False

		# So far, everything checks out for this node.  Check all of its children.
		for i in range(node.n + 1):
			if not self.is_btree_helper(node.c[i]):
				return False

		return True


# Testing
if __name__ == "__main__":

	import numpy as np

	# Small example.
	B_Tree1 = BTree(2)
	# Insert.
	B_Tree1.insert(5)
	print(B_Tree1)
	for i in range(8):
		B_Tree1.insert(2 * i)
		if not B_Tree1.is_btree():
			print("Bad B-tree:")
			print(B_Tree1)
	print(B_Tree1.is_btree())
	print(B_Tree1)
	# Search.
	obj5, index = B_Tree1.search(5)
	print(obj5, ":", index)
	print(obj5.key[index] == 5)
	# Delete element in root.
	B_Tree1.delete(5)
	print(B_Tree1.is_btree())
	print(B_Tree1)
	# Delete from root again.
	B_Tree1.delete(2)
	print(B_Tree1.is_btree())
	print(B_Tree1)
	# Delete from leaf.
	B_Tree1.delete(6)
	print(B_Tree1.is_btree())
	print(B_Tree1)

	# Large test case. 
	B_Tree2 = BTree(3)
	# Insert.
	array1 = np.arange(0, 50)
	np.random.shuffle(array1)
	for value in array1:
		B_Tree2.insert(value)
		if not B_Tree2.is_btree():
			print("Bad B-tree after inserting", value)
			print(B_Tree2)
	print(B_Tree2.is_btree())
	print(B_Tree2)
	np.random.shuffle(array1)
	for value in array1:
		B_Tree2.delete(value)
		if not B_Tree2.is_btree():
			print("Bad B-tree after deleting", value)
			print(B_Tree2)
