#!/usr/bin/env python3
# merge_sort.py

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

def merge(A, p, q, r):
	"""Merge two sorted sublists/subarrays to a larger sorted sublist/subarray.

	Arguments:
	A -- a list/array containing the sublists/subarrays to be merged
	p -- index of the beginning of the first sublist/subarray
	q -- index of the end of the first sublist/subarray;
	the second sublist/subarray starts at index q+1
	r -- index of the end of the second sublist/subarray
	"""
	# Copy the left and right sublists/subarrays.
	# If A is a list, slicing creates a copy.
	if type(A) is list:
		left = A[p: q+1]
		right = A[q+1: r+1]
	# Otherwise a is a np.array, so create a copy with list().
	else:
		left = list(A[p: q+1])
		right = list(A[q+1: r+1])

	i = 0    # index into left sublist/subarray
	j = 0    # index into right sublist/subarray
	k = p    # index into a[p: r+1]

	# Combine the two sorted sublists/subarrays by inserting into A
	# the lesser exposed element of the two sublists/subarrays.
	while i < len(left) and j < len(right):
		if left[i] <= right[j]:
			A[k] = left[i]
			i += 1
		else:
			A[k] = right[j]
			j += 1
		k += 1

	# After going through the left or right sublist/subarray, copy the 
	# remainder of the other to the end of the list/array.
	if i < len(left):  # copy remainder of left
		A[k: r+1] = left[i:]
	if j < len(right):  # copy remainder of right
		A[k: r+1] = right[j:]


def merge_sort(A, p=0, r=None):
	"""Sort the elements in the sublist/subarray a[p:r+1].

	Arguments:
	A -- a list/array containing the sublist/subarray to be merged
	p -- index of the beginning of the sublist/subarray (default = 0)
	r -- index of the end of the sublist/subarray (default = None)
	"""
	# If r is not given, set to the index of the last element of the list/array.
	if r is None:
		r = len(A) - 1
	if p >= r:  # 0 or 1 element?
		return
	q = (p+r) // 2            # midpoint of A[p: r]
	merge_sort(A, p, q)       # recursively sort A[p: q]
	merge_sort(A, q + 1, r)   # recursively sort A[q+1: r]
	merge(A, p, q, r)         # merge A[p: q] and A[q+1: r] into A[p: r]


# Testing
if __name__ == "__main__":
	
	import numpy as np

	# Repeating terms. 
	list1 = [11, 1, 51, 1, 5, 3]
	list1test = list(list1)
	merge_sort(list1)
	print(list1)
	print(list1 == sorted(list1test))

	# Empty list should return empty list. 
	list2 = []
	merge_sort(list2)
	print(list2)
	print(list2 == [])

	# Negative number. 
	list3 = [1, 1, -5, 6]
	list3test = list(list3)
	merge_sort(list3)
	print(list3)
	print(list3 == sorted(list3test))

	# Float and int, testing numpy array. 
	array1 = np.array([11, -4, 20, 15, 13.5, -20])
	array1test = np.copy(array1)
	merge_sort(array1)
	print(array1)
	print(np.array_equal(array1, np.sort(array1test)))

	# Already sorted array. 
	array2 = np.array(range(50))
	array2test = np.copy(array2)
	merge_sort(array2)
	print(array2)
	print(np.array_equal(array2, np.sort(array2test)))

	# Array in reversed sorted order. 
	array3 = np.arange(50, 0, -5)
	array3test = np.copy(array3)
	print("Before sorting: ", end = '')
	print(array3)
	merge_sort(array3)
	print("After sorting: ", end = '')
	print(array3)
	print(np.array_equal(array3, np.sort(array3test)))

	# Large array. 
	array4 = np.random.randint(-5000, 5000, size=1000)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	merge_sort(array4)
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(array4, np.sort(array4test)))
