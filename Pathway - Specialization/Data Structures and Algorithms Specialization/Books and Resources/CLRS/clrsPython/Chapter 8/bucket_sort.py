#!/usr/bin/env python3
# bucket_sort.py

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

from math import floor
from insertion_sort import insertion_sort


def bucket_sort(A, n):
	"""Sort an array or list of n elements distributed uniformly over [0, 1).
	
	Argument:
	A -- an array/list
	n -- length of A

	Returns:
	A sorted list 
	"""
	# Make B a list of n empty lists.
	B = [None] * n
	for i in range(n):
		B[i] = []

	# Distribute the n input numbers into n equal-sized subintervals
	for i in range(n):
		B[floor(n * A[i])].append(A[i])

	# Sort each subinterval. 
	for i in range(n):
		insertion_sort(B[i], len(B[i]))

	# Concatenate the lists b[0], b[1], ...b[n-1] together in order.
	return [x for sublist in B for x in sublist]


# Testing
if __name__ == "__main__":

	import numpy as np

	# Textbook example.
	list1 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
	list1test = list(list1)
	list1 = bucket_sort(list1, len(list1))
	print(list1)
	print(sorted(list1test) == list1)

	# Repeating terms. 
	list2 = [0.5, 0.5, 0.233, 0.76, 0.74, 0.21]
	list2test = list(list2)
	list2 = bucket_sort(list2, len(list2))
	print(list2)
	print(sorted(list2test) == list2)

	# Empty list. 
	list3 = []
	list3 = bucket_sort(list3, len(list3))
	print(list3)
	print(list3 == [])

	# Testing numpy array. 
	array1 = np.array([0.11, 0.4, 0.2, 0.15, 0.135, 0.20])
	array1test = np.copy(array1)
	array1 = bucket_sort(array1, len(array1))
	print(array1)
	print(np.array_equal(np.sort(array1test), array1))

	# Already sorted array. 
	array2 = np.arange(0, 1, 0.05)
	array2test = np.copy(array2)
	array2 = bucket_sort(array2, len(array2))
	print(array2)
	print(np.array_equal(np.sort(array2test), array2))

	# Array in reversed sorted order. 
	array3 = np.arange(0.99, 0, -.11)
	array3test = np.copy(array3)
	print("Before sorting: ", end = '')
	print(array3)
	array3 = bucket_sort(array3, len(array3))
	print("After sorting: ", end = '')
	print(array3)
	print(np.array_equal(np.sort(array3test), array3))

	# Large array. 
	array4 = np.random.uniform(0, 1, size=1000)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	array4 = bucket_sort(array4, len(array4))
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(np.sort(array4test), array4))
