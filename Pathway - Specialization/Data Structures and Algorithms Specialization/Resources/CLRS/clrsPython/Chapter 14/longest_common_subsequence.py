#!/usr/bin/env python3
# longest_common_subsequence.py

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

"""A subsequence of a given sequence is the given sequence with 0 or more elements left out.
"""

UP_AND_LEFT = "\u2196"  # northwest arrow
UP = "\u2191"           # up arrow
LEFT = "\u2190"         # left arrow

import numpy as np


def lcs_length(X, Y, m, n):
	"""Recursively compute the length of an LCS of two sequences.

	Arguments:
	X -- a sequence represented as a string or list/array
	Y -- another sequence represented as a string or list/array
	m -- length of X
	n -- length of Y

	Returns:
	c -- an array in which c[i, j] is the length of an LCS of the 
	sequences X[:i] and Y[:j]. Entries used are c[0:m+1, 0:n+1].
	b -- an array in which b[i, j] points to the table entry corresponding
	to the optimal subproblem solution chosen when computing c[i, j]. 
	Entries used are b[1:m+1, 1:n+1].
	"""

	b = np.empty(shape=[m+1, n+1], dtype=str)  # using indices 1:m+1, 1:n+1
	c = np.zeros(shape=[m+1, n+1])             # using indices 0:m+1, 0:n+1
	for i in range(1, m+1):  # fill row by row
		for j in range(1, n+1):
			# Subproblem of finding LCS of X[: i-1] and Y[: j-1].
			if X[i-1] == Y[j-1]:  # -1 for 0-origin indexing
				c[i, j] = c[i-1, j-1] + 1
				b[i, j] = UP_AND_LEFT
			# Consider two subproblems of finding an LCS of X[: i] and Y[: j - 1] and of X[: i - 1] and Y[: j].
			# Store max(c[i, j-1], c[i-1, j]).
			elif c[i-1, j] >= c[i, j-1]:
					c[i, j] = c[i-1, j]
					b[i, j] = UP
			else:
				c[i, j] = c[i, j-1]
				b[i, j] = LEFT

	return c, b


def print_lcs(b, X, i, j):
	"""Print an LCS of X and Y in the proper, forward order.

	Arguments:
	b -- an array in which b[i, j] points to the table entry corresponding
	to the optimal subproblem solution chosen when computing c[i, j]. 
	Entries used are b[1:m+1, 1:n+1].
	X -- a sequence represented as a string or list/array
	i -- length of first subsequence, on first call equals m
	j -- length of second subsequence, on first call equals n
	"""
	if i == 0 or j == 0:
		return 
	# Follow directions to print in proper, forward order.
	if b[i, j] == UP_AND_LEFT:
		print_lcs(b, X, i-1, j-1)
		print(X[i - 1], end ="")  # -1 for 0-origin indexing
	elif b[i, j] == UP:
		print_lcs(b, X, i-1, j)
	else:
		print_lcs(b, X, i, j-1)


# Testing
if __name__ == "__main__":

	from matrix_chain_multiply import print_table

	# Textbook example. 
	X = ["A", "B", "C", "B", "D", "A", "B"]
	Y = ["B", "D", "C", "A", "B", "A"]
	m = len(X)
	n = len(Y)
	c, b = lcs_length(X, Y, m, n)
	print_lcs(b, X, m, n)  # should be bcba
	print()
	print_table(c, 0, m, 0, n, int, whole_table=True)
	print_table(b, 1, m, 1, n, whole_table=True)

	# Larger example.
	X = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
	Y = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
	m = len(X)
	n = len(Y)
	c, b = lcs_length(X, Y, m, n)
	print_lcs(b, X, m, n)  # should be GTCGTCGGAAGCCGGCCGAA
	print()
