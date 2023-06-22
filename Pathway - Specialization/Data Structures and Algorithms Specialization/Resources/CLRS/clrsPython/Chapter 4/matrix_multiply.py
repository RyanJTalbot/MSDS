#!/usr/bin/env python3
# matrix_multiply.py

# Introduction to Algorithms, Fourth edition
# Tom Cormen

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

def matrix_multiply(A, B, C, n):
    """Compute C = C + (A * B), where A, B, and C are n x n matrices."""

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]


def matrix_multiply_recursive(A, B, C, n):
    """Compute C = C + (A * B), where A, B, and C are n x n matrices.
       n must be an exact power of 2."""

    # This method is a wrapper to verify that n is a power of 2, and
    # then calls the auxiliary recursive method to perform the matrix multiplication.
    if n > 0 and n & (n-1) == 0:
        matrix_multiply_recursive_aux(A, B, C, n, 0, 0, 0, 0, 0, 0)
    else:
        raise RuntimeError("Matrix dimension " + str(n) + " is not an exact power of 2.")


def matrix_multiply_recursive_aux(A, B, C, n, A_row, A_col, B_row, B_col, C_row, C_col):
    """Compute C = C + (A * B), where A, B, and C are n x n matrices.
       n is known to be an exact power of 2.

       Other parameters:
        A_row, A_col: starting row and column for the n x n submatrix of A
        B_row, B_col: starting row and column for the n x n submatrix of B
        C_row, C_col: starting row and column for the n x n submatrix of C
    """

    if n == 1:
        C[C_row, C_col] += A[A_row, A_col] * B[B_row, B_col]  # base case
        return
    half = n // 2
    matrix_multiply_recursive_aux(A, B, C, half, A_row, A_col, B_row, B_col, C_row, C_col)
    matrix_multiply_recursive_aux(A, B, C, half, A_row, A_col, B_row, B_col + half, C_row, C_col + half)
    matrix_multiply_recursive_aux(A, B, C, half, A_row + half, A_col, B_row, B_col, C_row + half, C_col)
    matrix_multiply_recursive_aux(A, B, C, half, A_row + half, A_col, B_row, B_col + half, C_row + half, C_col + half)
    matrix_multiply_recursive_aux(A, B, C, half, A_row, A_col + half, B_row + half, B_col, C_row, C_col)
    matrix_multiply_recursive_aux(A, B, C, half, A_row, A_col + half, B_row + half, B_col + half, C_row, C_col + half)
    matrix_multiply_recursive_aux(A, B, C, half, A_row + half, A_col + half, B_row + half, B_col, C_row + half, C_col)
    matrix_multiply_recursive_aux(A, B, C, half, A_row + half, A_col + half, B_row + half, B_col + half, C_row + half, C_col + half)


def strassen(A, B, C, n):
    """Compute C = C + (A * B), where A, B, and C are n x n matrices, using Strassen's method.
       n must be an exact power of 2."""

    # This method is a wrapper to verify that n is a power of 2, and
    # then calls the auxiliary recursive method to perform the matrix multiplication.
    if n > 0 and n & (n-1) == 0:
        return strassen_aux(A, B, C, n, 0, 0, 0, 0, 0, 0)
    else:
        raise RuntimeError("Matrix dimension " + str(n) + " is not an exact power of 2.")


def strassen_aux(A, B, C, n, A_row, A_col, B_row, B_col, C_row, C_col):
    """Compute C = C + (A * B), where A, B, and C are n x n matrices, using Strassen's method.
       n is known to be an exact power of 2.

       Other parameters:
        A_row, A_col: starting row and column for the n x n submatrix of A
        B_row, B_col: starting row and column for the n x n submatrix of B
        C_row, C_col: starting row and column for the n x n submatrix of C
        """

    if n == 1:
        C[C_row, C_col] += A[A_row, A_col] * B[B_row, B_col]  # base case
        return

    half = n // 2

    S1 = B[B_row: B_row + half, B_col + half: B_col + 2 * half] - B[B_row + half: B_row + 2 * half, B_col + half: B_col + 2 * half]
    S2 = A[A_row: A_row + half, A_col: A_col + half] + A[A_row: A_row + half, A_col + half: A_col + 2 * half]
    S3 = A[A_row + half: A_row + 2 * half, A_col: A_col + half] + A[A_row + half: A_row + 2 * half, A_col + half: A_col + 2 * half]
    S4 = B[B_row + half: B_row + 2 * half, B_col: B_col + half] - B[B_row: B_row + half  , B_col: B_col + half]
    S5 = A[A_row: A_row + half, A_col: A_col + half] + A[A_row + half: A_row + 2 * half, A_col + half: A_col + 2 * half]
    S6 = B[B_row: B_row + half, B_col: B_col + half] + B[B_row + half: B_row + 2 * half, B_col + half: B_col + 2 * half]
    S7 = A[A_row: A_row + half, A_col + half: A_col + 2 * half] - A[A_row + half: A_row + 2 * half, A_col + half: A_col + 2 * half]
    S8 = B[B_row + half: B_row + 2 * half, B_col: B_col + half] + B[B_row + half: B_row + 2 * half, B_col + half: B_col + 2 * half]
    S9 = A[A_row: A_row + half, A_col: A_col + half] - A[A_row + half: A_row + 2 * half, A_col: A_col + half]
    S10 = B[B_row: B_row + half, B_col: B_col + half] + B[B_row: B_row + half, B_col + half: B_col + 2 * half]

    P1 = np.zeros((half, half))
    P2 = np.zeros((half, half))
    P3 = np.zeros((half, half))
    P4 = np.zeros((half, half))
    P5 = np.zeros((half, half))
    P6 = np.zeros((half, half))
    P7 = np.zeros((half, half))

    strassen_aux(A, S1, P1, half, A_row, A_col, 0, 0, 0, 0)
    strassen_aux(S2, B, P2, half, 0, 0, B_row + half, B_col + half, 0, 0)
    strassen_aux(S3, B, P3, half, 0, 0, B_row, B_col, 0, 0)
    strassen_aux(A, S4, P4, half, A_row + half, A_col + half, 0, 0, 0, 0)
    strassen_aux(S5, S6, P5, half, 0, 0, 0, 0, 0, 0)
    strassen_aux(S7, S8, P6, half, 0, 0, 0, 0, 0, 0)
    strassen_aux(S9, S10, P7, half, 0, 0, 0, 0, 0, 0)

    C[C_row: C_row + half, C_col: C_col + half] = C[C_row: C_row + half, C_col: C_col + half] + P5 + P4 - P2 + P6
    C[C_row: C_row + half, C_col + half: C_col + 2 * half] = C[C_row: C_row + half, C_col + half: C_col + 2 * half] + P1 + P2
    C[C_row + half: C_row + 2 * half, C_col: C_col + half] = C[C_row + half: C_row + 2 * half, C_col: C_col + half] + P3 + P4
    C[C_row + half: C_row + 2 * half, C_col + half: C_col + 2 * half] = C[C_row + half: C_row + 2 * half, C_col + half: C_col + 2 * half] + P5 + P1 - P3 - P7


# Testing
if __name__ == "__main__":

    import numpy as np
    from matrix_inverse import almost_equal

    # Test non-recursive matrix multiplication.
    n = 8
    A = np.arange(n*n).reshape(n, n)
    print(A)
    B = np.zeros((n, n))
    # Make B be a permutation matrix for reversal.
    for i in range(n):
        B[i, n-1-i] = 1
    print(B)
    C = np.zeros((n, n))
    matrix_multiply(A, B, C, n)
    print(C)  # should be A with its columns in reverse order

    # Try with random numbers.
    rg = np.random.default_rng(1)
    A = rg.random((n, n))
    print(A)
    B = rg.random((n, n))
    print(C)
    C = np.ones((n, n))
    matrix_multiply(A, B, C, n)
    print(C)
    npC = A @ B  # multiply A and B in numpy
    npC += 1.0
    print(npC)
    print(almost_equal(C, npC, n))

    # Test recursive matrix multiplication.
    n = 8
    A = np.arange(n*n).reshape(n, n)
    print(A)
    B = np.zeros((n, n))
    # Make B be a permutation matrix for reversal.
    for i in range(n):
        B[i, n-1-i] = 1
    print(B)
    C = np.zeros((n, n))
    matrix_multiply_recursive(A, B, C, n)
    print(C)  # should be A with its columns in reverse order

    # Try with random numbers.
    rg = np.random.default_rng(1)
    A = rg.random((n, n))
    print(A)
    B = rg.random((n, n))
    print(B)
    C = np.ones((n, n))
    matrix_multiply_recursive(A, B, C, n)
    print(C)
    npC = A @ B  # multiply A and B in numpy
    npC += 1.0
    print(npC)
    print(almost_equal(C, npC, n))

    # Test for non-exact power of 2.
    n = 6
    A = np.arange(n*n).reshape(n, n)
    print(A)
    B = np.zeros((n, n))
    # Make B be a permutation matrix for reversal.
    for i in range(n):
        B[i, n-1-i] = 1
    print(B)
    C = np.zeros((n, n))
    try:
        matrix_multiply_recursive(A, B, C, n)
    except RuntimeError as e:
        print(e)

    # Test Strassen's method for matrix multiplication.
    n = 8
    A = np.arange(n*n).reshape(n, n)
    print(A)
    B = np.zeros((n, n))
    # Make B be a permutation matrix for reversal.
    for i in range(n):
        B[i, n-1-i] = 1
    print(B)
    C = np.zeros((n, n))
    strassen(A, B, C, n)
    print(C)  # should be A with its columns in reverse order

    # Try with random numbers.
    rg = np.random.default_rng(1)
    A = rg.random((n, n))
    print(A)
    B = rg.random((n, n))
    print(B)
    C = np.ones((n, n))
    strassen(A, B, C, n)
    print(C)
    npC = A @ B  # multiply A and B in numpy
    npC += 1.0
    print(npC)
    print(almost_equal(C, npC, n))
