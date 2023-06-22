#!/usr/bin/env python3
# lup.py

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


def LUP_solve(L, U, pi, b, n):
	"""Solve A system Ax = b of linear equations. A is given by its LUP decomposition: PA = LU.

	Arguments:
	L -- a unit lower-triangular matrix
	U -- an upper-triangular matrix
	pi -- the permutation such that the permutation matrix P has P[i, pi[i]] = 1 and P[i, j] = 0 for j != pi[i]
	b -- n values for solving Ax = b
	n -- all matrices are n x n, and all vectors have n elements

	Returns:
	x such that Ax = b, i.e., P^{-1}LU = b, where P^{-1} is the inverse of P
	"""
	x = [None] * n
	y = [None] * n

	# Solve y using forward substitution.
	for i in range(n):  # from 0 to n - 1
		y[i] = b[pi[i]]
		for j in range(i):
			y[i] -= L[i][j] * y[j]

	# Solve x using backward substitution.
	for i in range(n-1, -1, -1):  # from n-1 to down to 0
		sum = 0
		for j in range(i + 1, n):
			sum += U[i][j] * x[j]
		x[i] = (y[i] - sum) / U[i][i]
	return x


def LU_decomposition(A, n):
	"""Perform an LU decomposition of matrix A, so that A = LU.
	Assumption:
	No pivoting is needed. For example, A could be symmetric positive-definite.

	Argument: 
	A -- a numpy array or matrix
	n -- A is n x n

	Returns:
	L -- unit lower-triangular matrix as a numpy matrix
	U -- upper-triangular matrix as a numpy matrix
	"""
	A = np.copy(A)	# copy array
	L = np.zeros(shape=[n, n])  # unit lower-triangular matrix
	U = np.zeros(shape=[n, n])  # upper-triangular matrix

	for i in range(n):
		L[i, i] = 1  # 1s on the diagonal
	
	for k in range(n):
		U[k, k] = A[k, k]  # determine the pivot
		for i in range(k + 1, n):
			L[i, k] = A[i, k] / A[k, k]  # A[i, k] holds v[i]
			U[k, i] = A[k, i]            # A[k, i] holds w[i]

		# Compute the Schur complement and store it back into A.
		for i in range(k + 1, n):
			for j in range(k + 1, n):
				A[i, j] -= L[i, k] * U[k, j]

	return L, U


def LUP_decomposition(A, n):
	"""Perform an LUP decomposition of matrix A, so that PA = LU.

	Argument: 
	A -- a numpy array or matrix
	n -- A is n x n

	Returns:
	L -- unit lower-triangular matrix as a numpy matrix
	U -- upper-triangular matrix as a numpy matrix
	pi -- the permutation such that the permutation matrix P has P[i, pi[i]] = 1 and P[i, j] = 0 for j != pi[i]
	"""
	A = np.copy(A)  # copy the matrix
	pi = np.arange(n)  # initialize pi to the identity permutation

	for k in range(n):
		p = 0

		for i in range(k, n):  # find the largest absolute value in column k
			if abs(A[i, k]) > p:
				p = abs(A[i, k])
				k_prime = i  # row number of the largest found so far

		if p == 0:
			raise RuntimeError("Singular matrix")

		pi[k], pi[k_prime] = pi[k_prime], pi[k]
		for i in range(n):  # exchange rows k and k_prime
			A[k, i], A[k_prime, i] = A[k_prime, i], A[k, i]

		# Compute the Schur complement and store it back into A.
		for i in range(k + 1, n):
			A[i, k] /= A[k, k]		# pivot
			for j in range(k + 1, n):
				A[i, j] -= A[i, k] * A[k, j]  # compute L and U in place in A

	# Initialize L and U.
	L = np.zeros(shape=[n, n])  # unit lower-triangular matrix
	U = np.zeros(shape=[n, n])  # upper-triangular matrix

	for i in range(n):
		L[i, i] = 1  # 1s on the diagonal

	# Extract L and U from the Schur complement.
	for i in range(n):
		for j in range(n):
			if i > j: 
				L[i, j] = A[i, j]
			else:
				U[i, j] = A[i, j]

	return L, U, pi


def convert_perm_array_to_matrix(pi, n):
	""" Convert a permutation array pi of length n to an n x n permutation matrix P. """
	P = np.zeros(shape=[n, n], dtype=int)
	for i in range(n):
		P[i, pi[i]] = 1
	return P


# Testing
if __name__ == "__main__":

	# Be careful when using integers with numpy because it will automatically
	# convert floats derived from solving to integers.
	# Textbook example. 
	A = np.array([(2, 3, 1, 5), (6, 13, 5, 19), (2, 19, 10, 23), (4, 10, 11, 31)])
	n = len(A)
	print(A)
	L, U = LU_decomposition(A, n)
	# L should be [1 0 0 0; 3 1 0 0; 1 4 1 0; 2 1 7 1]
	print("L")
	print(L)
	# U should be [2 3 1 5; 0 4 2 4; 0 0 1 2; 0 0 0 3]
	print("U")
	print(U)
	print()

	# Textbook example. 
	A = np.array([(2, 0, 2, 0.6), (3, 3, 4, -2), (5, 5, 4, 2), (-1, -2, 3.4, -1)])
	n = len(A)
	print(A)
	L, U, pi = LUP_decomposition(A, n)
	print("L")
	print(L)
	print("U")
	print(U)
	print("pi")
	print(pi)
	P = convert_perm_array_to_matrix(pi, n)
	print("P")
	print(P)
	print(np.array_equal(P @ A, L @ U))  # verify decomposition
	print()

	# Solve. 
	A = np.array([(1.0, 2.0, 0.0), (3.0, 4.0, 4.0), (5.0, 6.0, 3.0)])
	n = len(A)
	print(A)
	b = (3, 7, 8)
	L, U, pi = LUP_decomposition(A, n)
	# L should be [1 0 0; 0.2 1 0; 0.6 0.5 1]
	print("L")
	print(L)
	# U should be [5 6 3; 0 0.8 -0.6; 0 0 2.5]
	print("U")
	print(U)
	print("pi")
	print(pi) 	# pi should be [2 0 1]
	# P should be [0 0 1; 1 0 0; 0 1 0]
	P = convert_perm_array_to_matrix(pi, n)
	print(P)
	print(np.array_equal(P @ A, L @ U))  # verify decomposition
	# Should be [-1.4, 2.2, 0.6]
	x = LUP_solve(L, U, pi, b, n)
	print(x)  # rounding error
	print(A @ x)  # should be [3, 7, 8]
