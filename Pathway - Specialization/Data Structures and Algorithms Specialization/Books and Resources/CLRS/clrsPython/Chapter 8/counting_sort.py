#!/usr/bin/env python3
# counting_sort.py

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


def counting_sort(A, n, k, get_key_func=None):
	"""Sort a list or numpy array of elements between 0 and k by counting.
	Differs from implementation

	Arguments:
	A -- a list/array to be sorted
	n -- length of A
	k -- upper bound for value of elements
	get_key_func -- an optional function that returns the key for the
		objects stored. If given, may be a static function in the object class. If
		omitted, then identity function is used.

	Returns:
	A list holding the sorted output.
	"""
	if get_key_func is None:
		get_key = lambda x: x
	else:
		get_key = get_key_func

	# Initialize C to be an array of 0s.
	C = np.zeros(shape=[k+1], dtype=int)

	# Count each input element. 
	for value in A:
		C[get_key(value)] += 1
	# C[i] now contains the number of elements equal to i.

	# Count how many input elements <= i. 
	for i in range(1, k+1):
		C[i] += C[i-1]
	# C[i] now contains the number of elements <= i.

	B = [None] * n
	# Place each element into its correct sorted position in B.
	for j in range(n-1, -1, -1):  # n - 1 down to 0
		key = get_key(A[j])
		B[C[key]-1] = A[j]  # -1 to adjust for 0-origin indexing
		C[key] -= 1

	return B


# Testing
if __name__ == "__main__":
	from key_object import KeyObject

	# Textbook example.
	a = [2, 5, 3, 0, 2, 3, 0, 3]
	n = len(a)
	b = counting_sort(a, n, 5)
	print(b)
	print(sorted(a) == b)

	# Large random array within range 0 to 49.
	array1 = np.random.randint(0, 50, size=1000)
	n = array1.size
	print("Before sorting: ", end='')
	print(array1)
	array2 = np.array(counting_sort(array1, n, 49))
	print("After sorting: ", end='')
	print(array2)
	print(np.array_equal(np.sort(array1), array2))

	# Example with objects.  Textbook example, but with letters in objects.
	a = [KeyObject('a', 2), KeyObject('b', 5), KeyObject('c', 3), KeyObject('d', 0),
			KeyObject('e', 2), KeyObject('f', 3), KeyObject('g', 0), KeyObject('h', 3)]
	n = len(a)
	b = counting_sort(a, n, 5, KeyObject.get_key)
	print([str(obj) for obj in b])  # should be d, g, a, e, c, f, h, b
