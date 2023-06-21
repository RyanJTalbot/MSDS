#!/usr/bin/env python3
# randomized_quicksort.py

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

from random import randint
from quicksort import partition


def randomized_partition(A, p, r):
	"""Rearrange A[p: r+1] into two (possible empty) sublists/subarrays
	such that all elements of a[p: q] <= a[q] <= a[q+1: r+1].  The pivot
	is chosen randomly from the elements of A[p: r+1].

	Arguments:
	A -- a list or numpy array to be sorted
	p -- index of the beginning of the sublist/subarray
	r -- index of the end of the sublist/subarray

	Returns:
	The index where the pivot ends up.
	"""
	i = randint(p, r)  # random index from p to r
	# Exchange a[r] with a[i], so new pivot is a[i].
	A[i], A[r] = A[r], A[i]  # exchange A[r] with A[i], so that A[i] becomes the pivot

	return partition(A, p, r)


def randomized_quicksort(A, p=0, r=None):
	"""Recursively sort a list or numpy array with a randomly selected pivot.

	Arguments:
	A -- a list or numpy array
	p -- index of the beginning of the sublist or subarray
	r -- index of the end of the sublist or subarray
	"""
	# The initial call to quicksort sets r to the last index.
	if r is None:
		r = len(A) - 1
	if p < r:
		# Partition around the randomly chosen pivot, which ends up in A[q].
		q = randomized_partition(A, p, r)
		randomized_quicksort(A, p, q-1)  # recursively sort the low side
		randomized_quicksort(A, q+1, r)  # recursively sort the high side


# Testing
if __name__ == "__main__":

	import numpy as np

	# Repeating terms. 
	list1 = [11, 1, 51, 1, 5, 3]
	list1test = list(list1)
	randomized_quicksort(list1)
	print(list1)
	print(list1 == sorted(list1test))

	# Empty list should return empty list. 
	list2 = []
	randomized_quicksort(list2)
	print(list2)
	print(list2 == [])

	# Negative number. 
	list3 = [1, 1, -5, 6]
	list3test = list(list3)
	randomized_quicksort(list3)
	print(list3)
	print(list3 == sorted(list3test))

	# Float and int, testing numpy array. 
	array1 = np.array([11, -4, 20, 15, 13.5, -20])
	array1test = np.copy(array1)
	randomized_quicksort(array1)
	print(array1)
	print(np.array_equal(array1, np.sort(array1test)))

	# Already sorted array. 
	array2 = np.array(range(50))
	array2test = np.copy(array2)
	randomized_quicksort(array2)
	print(array2)
	print(np.array_equal(array2, np.sort(array2test)))

	# Array in reversed sorted order. 
	array3 = np.arange(50, 0, -5)
	array3test = np.copy(array3)
	print("Before sorting: ", end = '')
	print(array3)
	randomized_quicksort(array3)
	print("After sorting: ", end = '')
	print(array3)
	print(np.array_equal(array3, np.sort(array3test)))

	# Large array. 
	array4 = np.random.randint(-5000, 5000, size=1000)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	randomized_quicksort(array4)
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(array4, np.sort(array4test)))