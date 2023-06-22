#!/usr/bin/env python3
# randomized_select.py

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

from randomized_quicksort import randomized_partition


def randomized_select(A, p, r, i):
	"""Return the ith smallest element of the array A[p:r+1]

	Arguments:
	A -- a sublist or subarray
	p -- index of the beginning of the sublist or subarray
	r -- index of the end of the sublist or subarray
	i -- ordinal number for ith smallest
	"""
	if p == r:
		return A[p]  # 1 <= i <= r-p+1 when p == r means that i = 1
	# Partition a such that each element of A[p: q] <= A[q]
	# and each element of A[q+1: r+1] >= A[q].
	q = randomized_partition(A, p, r)
	k = q - p + 1  # k is the number of elements in A[p: q+1]
	if i == k:  # the pivot value is the answer
		return A[q]
	elif i < k:
		return randomized_select(A, p, q-1, i)  # the ith smallest element is in A[p: q]
	else:
		return randomized_select(A, q+1, r, i-k)  # the ith smallest element is in A[q+1:r+1]


# Testing
if __name__ == "__main__":

	import numpy as np

	# 10th smallest value in range is -91.
	rng = np.random.default_rng()
	array1 = np.arange(-100, 100)
	rng.shuffle(array1)
	print(array1)
	min10 = randomized_select(array1, 0, array1.size - 1, 10)
	print(min10)
	print(min10 == -91)

	# 100th smallest value in range is -1.
	min100 = randomized_select(array1, 0, array1.size - 1, 100)
	print(min100)
	print(min100 == -1)

	# i can be larger than len(a)
	list2 = [1]
	print(list2)
	print(randomized_select(list2, 0, len(list2) - 1, 10))  # should be 1
