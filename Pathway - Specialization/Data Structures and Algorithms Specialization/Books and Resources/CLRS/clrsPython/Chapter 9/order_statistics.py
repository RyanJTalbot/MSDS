#!/usr/bin/env python3
# order_statistics.py

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

from math import ceil
from quicksort import partition


def partition_around(A, p, r, x):
	"""Partition A[p : r+1] around the pivot x.
	Rearrange A into two (possible empty) sublists/subarrays
	such that all elements of A[p:q] <= A[q] <= A[q+1:r+1].

	Arguments:
	A -- a list or numpy array to be sorted
	p -- index of the beginning of the sublist/subarray
	r -- index of the end of the sublist/subarray
	x -- value to partition around, must be present in A

	Returns:
	index of the pivot after partitioning
	"""
	# Find the index of the pivot value x. If x appears multiple times,
	# the first occurrence will do.
	i = p
	while A[i] != x:
		i += 1

	# Swap A[i] with A[r].
	A[i], A[r] = A[r], A[i]

	# Now just use regular partition.
	return partition(A, p, r)


def strided_insertion_sort_five(A, p, g):
	"""Run insertion sort on A[p], A[p+g], A[p+2g], A[p+3g], A[p+4g] in place.

	Arguments:
	A -- a list or numpy array
	p -- starting index in A
	g -- the stride for elements in A
	"""
	for i in range(1, 5):
		key = A[p + i*g]
		# Insert A[p + i*g] into sorted A[p], A[p + i], ..., A[p + (i-1)*g].
		j = i - 1
		while j >= 0 and A[p + j*g] > key:
			A[p + (j + 1)*g] = A[p + j*g]
			j -= 1
		A[p + (j + 1)*g] = key


def select(A, p, r, i):
	"""Return the ith smallest element of a.

	Arguments:
	A -- a list or array
	p -- index of the beginning of the sublist or subarray
	r -- index of the end of the sublist or subarray
	i -- ordinal number for ith smallest
	Assumption:
	A has at least i elements
	"""
	while (r-p+1) % 5 != 0:
		for j in range(p+1, r+1):  # put the minimum into A[p]
			if A[p] > A[j]:
				A[p], A[j] = A[j], A[p]

		# If want the minimum of A[p : r+1], we're done.
		if i == 1:
			return A[p]
		# Otherwise, we want the (i-1)st smallest element of A[p+1 : r+1].
		p += 1
		i -= 1

	g = (r-p+1) // 5         # number of 5-element groups
	for j in range(p, p+g):  # sort each group
		strided_insertion_sort_five(A, p, g)

	# All group medians now lie in the middle fifth of a[p : r+1].
	# Find the pivot x recursively as the median of group medians.
	x = select(A, p + 2*g, p + 3*g - 1, ceil(g / 2))
	q = partition_around(A, p, r, x)  # partition around the pivot

	# The rest is like the end of randomized_select.
	k = q - p + 1  # k is the number of elements in a[p:q+1]
	if i == k:
		return A[q]  # the pivot value is the answer
	elif i < k:
		return select(A, p, q - 1, i)  # ith smallest is in first half
	else:
		return select(A, q + 1, r, i - k)  # ith smallest is in second half


def find_median(A):
	"""Return median of an array or list A by sorting and taking the midpoint."""
	from insertion_sort import insertion_sort

	insertion_sort(A, len(A))
	return A[(len(A) - 1) // 2]  # return the middle number of sorted array


# Testing
if __name__ == "__main__":

	import numpy as np

	for upper in range(5, 30):
		array1 = np.arange(-5, upper)
		np.random.shuffle(array1)
		print(array1)
		print(select(array1, 0, len(array1) - 1, 6))  # should be 0

	list1 = [0, -55, 2, 3]
	print(list1)
	print(select(list1, 0, len(list1) - 1, 3))  # should be 2

	array2 = np.arange(-1000, 1000)
	np.random.shuffle(array2)
	print(array2)
	print(select(array2, 0, len(array2) - 1, 1))     # should be -1000
	print(select(array2, 0, len(array2) - 1, 1000))  # should be -1

	list2 = [1]
	print(list2)
	print(select(list2, 0, len(list2) - 1, 1))       # should be 1

	# Array of random integers.
	n = 37
	array3 = np.random.randint(0, 7000, size=n)
	print(array3)
	median3 = select(array3, 0, n-1, (n+1) // 2)
	print(sorted(array3))
	sorted_median3 = find_median(array3)
	print(median3, sorted_median3, median3 == sorted_median3)
