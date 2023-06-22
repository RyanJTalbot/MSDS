#!/usr/bin/env python3
# optimal_BST.py

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

import numpy as np
from print_table import print_table


def optimal_BST(p, q, n):
	""" Construct a binary search tree whose expected search cost is smallest. 

	Arguments:
	p -- array of probabilities of succesful searches. p[i] is the
	probability that a search will be for k[i], where k is the sequence
	of n distinct keys in sorted order. Entries used are p[1:n+1], and
	p[0] = 0. 
	q -- array of probabilities of unsuccessful searches. q[i] is the
	probability that a search falls between keys k[i] and k[i+1]. q[0] 
	is the probability that a search falls to the left of k[i] and q[n]
	is the probability that a search falls to the right of k[n]. Entries
	used are q[0:n+1].
	n -- number of distinct keys
	Returns:
	e -- the cost of an optimal solution for keys k[i] to k[j]. Entries used
	are e[1:n+2][0:n+1].
	root -- the root of an optimal binary search tree for each subproblem. root[i, j]
	is the root of an optimal binary search tree containing the keys k[i]
	to k[j]. The table uses only entries for which 1 <= i <= j <= n.
	"""

	e = np.zeros(shape=[n+2, n+1])
	# w[i][j] is the sum of probabilities p[i] through p[j] and 
	# q[i - 1] through q[j]. The entries used are w[1:n+2][0:n+1]
	# where j >= i -1. 
	w = np.empty(shape=[n+2, n+1])	
	root = np.zeros(shape=[n+1, n+1], dtype=int)
	# Initialize base cases of e and w.
	for i in range(1, n+2):
		e[i, i-1] = q[i-1]  # equation (14.14)
		w[i, i-1] = q[i-1]
	# Use recurrences to compute e[i, j] and w[i, j].
	for l in range(1, n+1):
		for i in range(1, n-l+2):
			j = i + l - 1
			e[i, j] = float('inf')
			w[i, j] = w[i, j-1] + p[j] + q[j]  # equation (14.15)
			for r in range(i, j+1):  # try all possible roots r
				t = e[i, r-1] + e[r+1, j] + w[i, j]  # equation (14.14)
				if t < e[i, j]:  # new minimum?
					e[i, j] = t
					root[i, j] = r
	return e, root


def print_e(e):
	"""Format and print the e table.

	Argument:
	e -- the cost of an optimal solution for keys k[i] to k[j]. Entries used are
	within e[1:n+2][0:n+1] where j >= i - 1. 
	"""
	print_table(e, 1, len(e) - 1, 0, len(e) - 2, lambda x: round(x, 2))


def print_root(root):
	"""Format and print the root table.

	Argument:
	root -- the root of an optimal binary search tree for each subproblem. root[i, j]
	is the root of an optimal binary search tree containing the keys k[i]
	to k[j]. The table only uses entries for which 1 <= i <= j <= n.
	"""
	print_table(root, 1, len(root) - 1, 1, len(root) - 1, int)


# Testing
if __name__ == "__main__":

	# Example from textbook.
	p = [0,  0.15, 0.10, 0.05, 0.10, 0.20]  # entry 0 unused
	q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
	e, root = optimal_BST(p, q, len(p) - 1)

	print_e(e) 	# roundoff error
	print()
	print_root(root)
