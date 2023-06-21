#!/usr/bin/env python3
# least_squares_approximation.py

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

import numpy as np
from matrix_inverse import matrix_inverse


def rectangular_matrix_multiply(A, B, p, q, r):
	"""Return C = A * B, where A is p x q, B is q x r, and C is p x r."""

	C = np.zeros(shape=(p, r))

	for i in range(p):
		for j in range(r):
			for k in range(q):
				C[i, j] += A[i, k] * B[k, j]

	return C


def least_squares_approximation(data, n):
	"""Return the coefficient vector for a function for a set of data
	points such that the approximation errors are small. 

	Arguments:
	data -- list of pairs of data points
	n -- degree of the polynomial approximation
	"""
	m = len(data)
	x = np.empty(shape=[m, 1])		# multi-dimensions needed for multiplication
	y = np.empty(shape=[m, 1])		# multi-dimensions needed for multiplication
	A = np.empty(shape=[m, n + 1]) 	# A[i, j] is x[i]**j
	A[:, 0].fill(1)					# fill first column with 1 (x ^ 0)

	for i in range(m):
		# Extract x and y from data. 
		x[i] = data[i][0]
		y[i] = data[i][1]
		# Compute matrix A.
		for j in range(1, n + 1):
			for i in range(m):
				A[i, j] = A[i, j-1] * x[i]  # A[i, j] = x[i] ** j

	# Compute the pseudoinverse A+.
	transpose = np.transpose(A)  # transpose is n+1 x m
	A_plus = rectangular_matrix_multiply(matrix_inverse(rectangular_matrix_multiply(transpose, A, n+1, m, n+1), n+1),
										 transpose, n+1, n+1, m)

	# Return the solution to A+ * y
	return rectangular_matrix_multiply(A_plus, y, n+1, m, 1)


# Testing
if __name__ == "__main__":

	# Textbook example.
	data = [(-1, 2), (1, 1), (2, 1), (3, 0), (5, 3)]
	print(least_squares_approximation(data, 2))
