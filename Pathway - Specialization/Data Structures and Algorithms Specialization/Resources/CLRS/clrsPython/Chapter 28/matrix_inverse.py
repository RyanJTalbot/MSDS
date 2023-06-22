#!/usr/bin/env python3
# matrix_inverse.py

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
from lup import LUP_solve, LUP_decomposition


def matrix_inverse(A, n):
	"""Return the inverse of matrix A using LUP decomposition.

	Argument:
	A -- numpy matrix or array
	n -- a is n x n
	"""
	L, U, pi = LUP_decomposition(A, n)
	A_inverse = np.empty(shape=[n, n])  # initialize inverse
	identity = np.eye(n)  # A * inverse should be identity
	for i in range(n):
		# Solve each column individually.
		A_inverse[:,i] = LUP_solve(L, U, pi, identity[:, i], n)
	return A_inverse


def almost_equal(A, B, n):
	"""Determine whether two n x n matrices are equal to within 1e-13 in each position."""
	for i in range(n):
		for j in range(n):
			if abs(A[i, j] - B[i, j]) > 1e-13:
				return False  # too far apart in row i, column n
	return True  # close enough in all positions


# Testing
if __name__ == "__main__":
	
	# Inverse. 
	# Make sure the numpy array for A has dtype float.
	A = np.array([(2.0, 3, 1, 5), (6, 13, 5, 19), (2, 19, 10, 23), (4, 10, 11, 31)])
	n = len(A)
	A_inverse = matrix_inverse(A, n)
	print(A)
	print(A_inverse)
	# @ is matrix multiplication for numpy arrays.
	product = A @ A_inverse  # should be identity excluding rounding error
	identity = np.eye(n)
	print(almost_equal(product, identity, n))
	print()

	# Random.
	n = 20
	A = np.random.random(size=(n, n))  # 20 by 20 array of [0.0, 1.0).
	A = A * 50
	A_inverse = matrix_inverse(A, n)
	print(A)
	print(A_inverse)
	# @ is matrix multiplication for numpy arrays.
	product = A @ A_inverse  # should be identity excluding rounding error
	print(product)
	identity = np.eye(n)
	print(almost_equal(product, identity, n))
