#!/usr/bin/env python3
# radix_sort.py

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
from math import log


def digit_counting_sort(A, B, n, r, i):
	"""Sort a list or numpy array of elements by the given radix 
	and number of digits.

	Arguments:
	A -- a list/array to be sorted
	B -- a list/array that holds the sorted output
	n -- length of A and B
	r -- radix
	i -- place value of each digit
	Assumption:
	The list or array consists only of integers >= 0.
	"""
	# Initialize C to be an array of 0s.
	C = np.zeros(shape=[r], dtype=int)

	denominator = r ** i

	# Count each input element. 
	for value in A:
		index = (value // denominator) % r
		C[index] += 1
	# C[i] now contains the number of elements equal to i.

	# Count how many input elements <= i. 
	for j in range(1, r):
		C[j] += C[j-1]
	# C[i] now contains the number of elements <= i.

	# Place each element into its correct sorted position in B.
	for j in range(n-1, -1, -1):
		index = (A[j] // denominator) % r
		B[C[index]-1] = A[j]
		C[index] -= 1


def bit_counting_sort(A, B, n, r, i, k, mask):
	"""Sort a list or numpy array of elements by the given radix that is a power of 2 and number of digits.

	Arguments:
	A -- a list/array to be sorted
	B -- a list/array that holds the sorted output
	n -- length of A and B
	r -- radix
	i -- place value of each digit
	k -- base-2 log of the radix
	mask -- integer that defines which bits to keep, only k rightmost bits are 1
	Assumptions: 
	The list or array consists only of integers >= 0.
	"""
	# Initialize C to be an array of zeros.
	C = np.zeros(shape=[r], dtype=int)

	shift = k * i  # shift k bits over at a time

	# Apply counting sort to k bits.
	# Count each input element. 
	for value in A:
		# Shift bits to the right by a factor of k and keep the rightmost leftover k bits.
		C[(value >> shift) & mask] += 1
	# C[i] now contains the number of elements equal to i.

	# Count how many input elements <= i. 
	for j in range(1, r):
		C[j] += C[j-1]
	# C[i] now contains the number of elements <= i.

	# Place each element into its correct sorted position in B.
	for j in range(n-1, -1, -1):
		index = (A[j] >> shift) & mask
		B[C[index]-1] = A[j]
		C[index] -= 1


def radix_sort_power_of_two(A, B, n, d, r):
	"""Sort a list or numpy array of elements by the given radix,
	which must be a power of 2, and number of digits.

	Arguments:
	A -- a list/array to be sorted
	B -- a list/array that holds the sorted output
	n -- length of A and B
	d -- number of digits
	r -- radix that is a power of two
	Assumptions: 
	The list or array consists only of integers >= 0.
	"""
	k = int(log(r, 2))   # base-2 log of the radix
	mask = (1 << k) - 1  # mask used to extract a subset of bits

	# From lowest order to highest order digit.
	for i in range(d):
		# Sort the most recently sorted array by the next digit. 
		if i % 2 == 0:  # alternating array to sort and output array
			bit_counting_sort(A, B, n, r, i, k, mask)
		else:           # next iteration, sort the output array
			bit_counting_sort(B, A, n, r, i, k, mask)

	if d % 2 == 1:  # copy the output list to A only if d is odd
		for i in range(n):
			A[i] = B[i]


def radix_sort_standard(A, B, n, d, r):
	"""Sort a list or numpy array of elements by the given 
	radix, that is not a power of two, and number of digits.

	Arguments:
	a -- a list/array to be sorted
	B -- a list/array that holds the sorted output
	n -- length of A and B
	d -- number of digits
	r -- radix
	Assumptions: 
	The list or array consists only of integers >= 0.
	"""
	# From lowest order to highest order digit.
	for i in range(d):
		# Sort the most recently sorted array by the next digit. 
		if i % 2 == 0:  # alternating array to sort and output array
			digit_counting_sort(A, B, n, r, i)
		else:           # next iteration, sort the output array
			digit_counting_sort(B, A, n, r, i)

	if d % 2 == 1:  # copy output list to A only if d is odd
		for i in range(n):
			A[i] = B[i]


def radix_sort(A, n, d, r):
	"""Sort from least significant to most significant digit. 

	Arguments:
	a -- a list or array to be sorted
	n -- length of A
	d -- number of digits
	r -- radix
	"""
	B = [0] * n

	# Using counting sort as the stable sort.
	# If the radix is a power of 2, using a faster radix sort for powers of 2.
	if r & (r-1) == 0:
		radix_sort_power_of_two(A, B, n, d, r)
	else:
		radix_sort_standard(A, B, n, d, r)


# Testing
if __name__ == "__main__":

	# Textbook example. 
	list1 = [329, 457, 657, 839, 436, 720, 355]
	list1test = list(list1)
	radix_sort(list1, len(list1), 4, 8)
	print(list1)
	print(sorted(list1test) == list1)

	# Empty list. 
	list2 = []
	radix_sort(list2, 0, 0, 10)
	print(list2)
	print(list2 == [])

	# Float should induce error message.
	array1 = np.array([2, 4, 1, 5.5])
	try: 
		radix_sort(array1, len(array1), 1, 10)
		print(array1)
	except:
		print("Cannot sort.")

	# Already sorted array. 
	array2 = np.array(range(50))
	array2test = np.copy(array2)
	radix_sort(array2, len(array2), 2, 15)
	print(array2)
	print(np.array_equal(array2test, array2))

	# Power of 2. 
	array3 = np.random.randint(0, 1000, size = 100)
	array3test = np.copy(array3)
	radix_sort(array3, len(array3), 2, 32)
	print(array3)
	print(np.array_equal(sorted(array3test), array3))
	
	# Array in reversed sorted order. 
	array4 = np.arange(50, 0, -5)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	radix_sort(array4, len(array4), 2, 10)
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(np.sort(array4test), array4))

	# Large array with power of 2.  
	array5 = np.random.randint(0, 1000000, size=1000)
	array5test = np.copy(array5)
	print("Before sorting: ", end = '')
	print(array5)
	radix_sort(array5,len(array5),  5, 16)
	print("After sorting: ", end = '')
	print(array5)
	print(np.array_equal(np.sort(array5test), array5))
