#!/usr/bin/env python3
# minimum_and_maximum.py

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

def minimum_and_maximum(A, n):
	"""Simultaneously find the minimum and maximum of n values in A."""
	if n % 2 == 1:  # n is odd
		# Set both min and max to the first value, then process as pairs.
		mini, maxi = A[0]
		rest = 1  # Starting index of the rest of A.
	else:  # n is even
		# Determine initial values of min and max with the first comparison.
		mini, maxi = compare_pair(A, 0)
		rest = 2  # starting index of the rest of A
	# Process the rest of list/array in pairs.
	for i in range(rest, len(A), 2):
		pair_min, pair_max = compare_pair(A, i)
		# Compare pair's min and max with the current values.
		if mini > pair_min:
			mini = pair_min
		if maxi < pair_max:
			maxi = pair_max

	return mini, maxi


def compare_pair(A, i):
	"""Return a tuple (min, max) of pair of elements A[i] and A[i + 1]."""
	if A[i] <= A[i + 1]:
		return A[i], A[i + 1]
	else:
		return A[i + 1], A[i]


# Testing
if __name__ == "__main__":

	import numpy as np

	# Minimum value in range is -100. 
	array1 = np.arange(-100, 100)
	n = len(array1)
	np.random.shuffle(array1)
	min1, max1 = minimum_and_maximum(array1, n)
	print(min1, ",", max1)
	print(min1 == -100)
	print(max1 == 99)

	array2 = np.random.randint(100, size=10)
	n = len(array2)
	min2, max2 = minimum_and_maximum(array2, n)
	print(array2)
	print(min2, ",", max2)
