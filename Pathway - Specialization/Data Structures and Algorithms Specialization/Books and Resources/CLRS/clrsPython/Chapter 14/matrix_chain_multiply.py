#!/usr/bin/env python3
# matrix_chain_multiply.py

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

""" Given a chain of n matrices, fully parenthesize the product 
in a way that minimizes the number of scalar multiplications. 
"""

import numpy as np
from print_table import print_table

#!/usr/bin/env python3
# matrix_multiply.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao and Tom Cormen


def matrix_chain_multiply(A, B, C, p, q, r):
	"Compute C = C + (A * B), where A is p x q, B is q x r, and C is p x r."

	for i in range(p):
		for j in range(r):
			for k in range(q):
				C[i, j] += A[i, k] * B[k, j]


def matrix_chain_order(p, n):
	"""Determine the optimal number of scalar multiplications needed
	to compute the matrix chain product A[1] * A[2] * ... * A[n].

	Arguments: 
	p -- list of dimensions of matrices in which matrix i has dimensions p[i - 1] x p[i]
	n -- p has entries indexed 0 to n

	Returns:
	m -- array with m[i, j] as the lowest number of scalar multiplications
	to compute A(i..j). Entries used are m[1:n+1, 1:n+1].
	s -- array that records which position to split an optimal solution 
	to a subproblem of m[i, j]. Entries used are s[1:n, 2:n+1].
	"""
	m = np.zeros(shape=[n+1, n+1])           # using indices 1:n+1, 1:n+1
	s = np.zeros(shape=[n, n+1], dtype=int)  # using indices 1:n, 2:n+1

	for l in range(2, n + 1):          # l is the chain length
		for i in range(1, n - l + 2):  # chain begins at A[i]
			j = i + l - 1              # chain ends at A[j]
			m[i, j] = float('inf')
			for k in range(i, j):      # try splitting between A[k] and A[k+1]
				# m[i, j] cost depends on entries m[i, k] and m[k+1, j],
				# which are already computed.
				q = m[i, k] + m[k+1, j] + p[i-1] * p[k] * p[j]
				if q < m[i, j]:
					m[i, j] = q        # remember this cost
					s[i, j] = k        # remember this index
	return m, s


def print_optimal_parens(s, i, j):
	"""Print an optimal parenthesization of the matrix chain from A[i] to A[j].

	Assumption:
	Matrix A[i] has dimensions p[i-1] x p[i]
	"""
	if i == j:
		print("A[" + str(i), end = "]")
	else:
		print("(", end = "")
		print_optimal_parens(s, i, s[i, j])      # left side
		print_optimal_parens(s, s[i, j] + 1, j)  # right side
		print(")", end = "")


def recursive_matrix_chain(p, i, j):
	"""Determine recursively optimal number of scalar multiplications
	needed to compute the matrix chain product from A[i] to A[j].

	Arguments: 
	p -- array of dimensions of matrices in which matrix i has dimensions p[i - 1] x p[i]
	i -- index of the beginning matrix in the matrix subchain
	j -- index of the end matrix in the matrix subchain
	"""
	if i == j:
		return 0
	m[i, j] = float('inf')
	for k in range(i, j):
		# Recomputes m[i, j] every time.
		q = recursive_matrix_chain(p, i, k) + recursive_matrix_chain(p, k+1, j) + (p[i-1] * p[k] * p[j])
		if q < m[i, j]:
			m[i, j] = q  # store the current minimum
	return int(m[i, j])


def memoized_matrix_chain(p, n):
	"""Determine recursively optimal number of scalar multiplications
	needed to compute the matrix chain product for whole chain, using memoization.

	Arguments:
	p -- array of dimensions of matrices in which matrix i has dimensions p[i - 1] x p[i]
	n -- p has entries indexed 0 to n
	"""
	m = np.empty(shape=[n + 1, n + 1])
	m.fill(float('inf'))  # fill array elements with infinity
	return lookup_chain(m, p, 1, n)


def lookup_chain(m, p, i, j):
	"""Look up value for m[i, j] if it is already computed.  If not, compute the value and store it.

	Arguments: 
	m -- array with m[i, j] as the lowest number of scalar multiplications
	to compute A(i..j). Entries used are m[1:n+1, 1:n+1].
	p -- array of dimensions of matrices in which matrix i has dimensions p[i - 1] x p[i]
	i -- index of the beginning matrix in the matrix subchain
	j -- index of the end matrix in the matrix subchain
	"""
	if m[i, j] < float('inf'):
		return m[i, j]  # return previously computed m[i, j]
	if i == j:
		m[i, j] = 0  
	else:
		# This is the first request for the value of m[i, j].  Compute and store it.
		for k in range(i, j):
			q = lookup_chain(m, p, i, k) + lookup_chain(m, p, k+1, j) + (p[i-1] * p[k] * p[j])
			if q < m[i, j]:
				m[i, j] = q  # store the minimum
	return int(m[i, j])


def print_m(m, n):
	"""Format and print m table.

	Arguments:
	m -- array with m[i, j] as the lowest number of scalar multiplications
	to compute A(i:j). Entries used are m[1:n+1, 1:n+1].
	n -- size of m
	"""
	print_table(m, 1, n, 1, n, int)


def print_s(s, n):
	"""Print the values of s that are used.

	Arguments:
	s -- array that records which position to split an optimal solution 
	to a subproblem of m[i, j]. Entries used are s[1:n, 2:n+1].
	n -- size of s
	"""
	print_table(s, 1, n-1, 2, n, int)


# Testing
if __name__ == "__main__":

	# Matrix chain multiply example from textbook.
	p = [30, 35, 15, 5, 10, 20, 25]
	n = len(p)-1
	m, s = matrix_chain_order(p, n)
	print_optimal_parens(s, 1, n)  # should print ((A[1](A[2]A[3]))((A[4]A[5])A[6]))
	print()
	print_m(m, n)
	print_s(s, n)
	print(int(m[1, n]))

	# Recursive. 
	m = np.zeros(shape=[n + 1, n + 1])
	print(recursive_matrix_chain(p, 1, n))

	# Memoized. Same answer.
	m = np.zeros(shape=[n + 1, n + 1])
	print(memoized_matrix_chain(p, n))

	# Random example.
	n = 10
	p = np.random.randint(2, 100, size=n+1)
	m, s = matrix_chain_order(p, n)
	print_optimal_parens(s, 1, n)
	print()
	print_m(m, n)
	print_s(s, n)
	print(int(m[1, n]))

	# Recursive.
	m = np.zeros(shape=[n + 1, n + 1])
	print(recursive_matrix_chain(p, 1, n))

	# Memoized. Same answer.
	print(memoized_matrix_chain(p, n))
