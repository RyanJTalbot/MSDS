#!/usr/bin/env python3
# quicksort.py

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

def quicksort(A, p=0, r=None):
	"""Recursively sort a list or numpy array. 

	Arguments:
	A -- a list or numpy array
	p -- index of the beginning of the sublist or subarray
	r -- index of the end of the sublist or subarray
	"""
	# The initial call to quicksort sets r to the last index.
	if r is None:
		r = len(A) - 1
	if p < r:
		# Partition around the pivot, which ends up in A[q].
		q = partition(A, p, r)
		quicksort(A, p, q-1)  # recursively sort the low side
		quicksort(A, q+1, r)  # recursively sort the high side


def partition(A, p, r):
	"""Rearrange A[p: r+1] into two (possible empty) sublists/subarrays
	such that all elements of a[p: q] <= a[q] <= a[q+1: r+1].
	A[r] is chosen as the pivot.

	Arguments: 
	A -- a list or numpy array to be sorted
	p -- index of the beginning of the sublist/subarray
	r -- index of the end of the sublist/subarray

	Returns:
	The index where the pivot ends up.
	"""
	x = A[r]  # select the last element as the pivot

	i = p - 1  # highest index into the low side
	for j in range(p, r):  # process each element other than the pivot
		if A[j] <= x:  # does this element belong on the low side?
			i += 1  # index of a new slot in the low side
			A[i], A[j] = A[j], A[i]  # put this element there

	A[i + 1], A[r] = A[r], A[i + 1]  # the pivot does just to the right of the low side
	return i + 1  # return the new index of the pivot


# To test hoare_partition, replace the call to partition in quicksort
# by a call to hoare_partition, and change the first recursive call
# to quicksort by quicksort(A, p, q).
def hoare_partition(A, p, r):
	"""Rearrange A into two (possible empty) sublists/subarrays
	such that all elements of a[p: j+1] <= a[j+1: r+1].

	Arguments:
	A -- a list or numpy array to be sorted
	p -- index of the beginning of the sublist/subarray
	q -- index of the end of the sublist/subarray

	Returns:
	j -- index of dividing point
	"""
	x = A[p]
	i = p-1
	j = r+1
	while True:
		while True:  # Python version of repeat-until loop
			j -= 1
			if A[j] <= x:
				break

		while True:  # Another repeat-until loop
			i += 1
			if A[i] >= x:
				break

		if i < j:
			A[i], A[j] = A[j], A[i]
		else:
			return j


# Testing
if __name__ == "__main__":

	import numpy as np

	# Repeating terms. 
	list1 = [11, 1, 51, 1, 5, 3]
	list1test = list(list1)
	quicksort(list1)
	print(list1)
	print(list1 == sorted(list1test))

	# Empty list should return empty list. 
	list2 = []
	quicksort(list2)
	print(list2)
	print(list2 == [])

	# Negative number. 
	list3 = [1, 1, -5, 6]
	list3test = list(list3)
	quicksort(list3)
	print(list3)
	print(list3 == sorted(list3test))

	# Float and int, testing numpy array. 
	array1 = np.array([11, -4, 20, 15, 13.5, -20])
	array1test = np.copy(array1)
	quicksort(array1)
	print(array1)
	print(np.array_equal(array1, np.sort(array1test)))

	# Already sorted array. 
	array2 = np.array(range(50))
	array2test = np.copy(array2)
	quicksort(array2)
	print(array2)
	print(np.array_equal(array2, np.sort(array2test)))

	# Array in reversed sorted order. 
	array3 = np.arange(50, 0, -5)
	array3test = np.copy(array3)
	print("Before sorting: ", end = '')
	print(array3)
	quicksort(array3)
	print("After sorting: ", end = '')
	print(array3)
	print(np.array_equal(array3, np.sort(array3test)))

	# Large array. 
	array4 = np.random.randint(-5000, 5000, size=1000)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	quicksort(array4)
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(array4, np.sort(array4test)))
