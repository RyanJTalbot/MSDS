#!/usr/bin/env python3
# disjoint_set_forest.py

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

class ForestNode:

	def __init__(self, data):
		"""Initialize forest node with itself as a parent adn rank 0."""
		self.data = data
		# The root is its own parent and is the representative.
		self.parent = self
		self.rank = 0

	def __str__(self):
		"""Return the string representation of the data in this node."""
		return str(self.data)


def make_set(x):
	"""Make a singleton set containing object x."""
	return ForestNode(x)


def find_set(x):
	"""Return the object that serves as the root of the set containing x."""
	if x != x.parent:  # the root is its own parent
		x.parent = find_set(x.parent)
	return x.parent  # return the root


def union(x, y):
	"""Unite set with x and set with y. The original sets are destroyed.

	Arguments:
	x -- an object within a set
	y -- an object within another set
	"""
	link(find_set(x), find_set(y))


def link(x, y):
	"""Link together two sets, given their root nodes. 

	Arguments:
	x -- the root node of one set
	y -- the root node of another set
	"""
	# The root with larger rank becomes the parent of the root with the smaller rank.
	if x.rank > y.rank:
		y.parent = x  # x becomes the parent
	else: 
		x.parent = y  # y becomes the parent
		if x.rank == y.rank:
			y.rank += 1


def print_find_path(x):
	"""Print the find path starting from node x to the root."""
	while x != x.parent:
		print(x, end="->")
		x = x.parent
	print(x)


# Testing
if __name__ == "__main__":

	# Set union.
	set1 = make_set(1)
	set2 = make_set(2)
	union(set1, set2)
	print_find_path(set1) 	# root is 2
	print(find_set(set1))

	sets = []
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	for letter in letters:
		sets.append(make_set(letter))
	i = 0
	while i < len(letters):
		union(sets[i], sets[i+1])
		i += 2
	for s in sets:
		print_find_path(s)
	i = 0
	while i < len(letters):
		union(sets[i], sets[i+2])
		i += 4
	for s in sets:
		print_find_path(s)
	union(sets[0], sets[4])
	for s in sets:
		print_find_path(s)
