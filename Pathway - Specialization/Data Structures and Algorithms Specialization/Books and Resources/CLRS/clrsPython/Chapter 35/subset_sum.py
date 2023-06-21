#!/usr/bin/env python3
# subset_sum.py

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

def exact_subset_sum(S, n, t):
	"""Return sum of subset of S that is closest to but does not exceed t. 

	Arguments:
	S -- a list of positive integers in arbitrary order
	n -- length of S
	t -- the target value
	"""
	L = [0]  # list of sums of all subsets of S that do not exceed t

	# Add each subset.
	for i in range(n):
		L = merge_lists(L, [x + S[i] for x in L])
		L = [y for y in L if y <= t]  # remove from L every element greater than t

	return L[-1]  # return the largest value in L


def approx_subset_sum(S, n, t, epsilon):
	"""Return the sum of the subset of S that is closest to but does not exceed t.

	Arguments:
	S -- list of positive integers in arbitrary order
	n -- length of S
	t -- target integer
	epsilon -- approximation parameter such that 0 < epsilon < 1

	Returns:
	the sum of a subset of S that is within a 1 + epsilon factor of the optimal solution
	"""
	L = [0]

	for i in range(n):
		L = merge_lists(L, [x + S[i] for x in L])
		# Trim to decrease the number of elements while keeping a close representative.
		L = trim(L, epsilon / (2*n))
		L = [y for y in L if y <= t]  # remove from L every element greater than t

	return L[-1]  # return the largest value in L


def trim(L, delta):
	"""Trim a sorted list L by delta by removing as many elements from L as possible.
	For every element y that was removed, there is an element z
	that approximates y, that is, y/(1 + delta) <= z <= y.

	Arguments: 
	L -- a sorted list
	delta -- the trimming parameter such that 0 < delta < 1

	Returns:
	L_prime -- the trimmed down list
	"""
	m = len(L)
	L_prime = [L[0]]  # start with the first element
	last = L[0]
	for i in range(1, m):
		if L[i] > (last * (1 + delta)):  # y[i] >= last because L is sorted
			L_prime.append(L[i])
			last = L[i]

	return L_prime


def merge_lists(L1, L2):
	"""Merge two sorted lists into a single list.

	Arguments:
	L1, L2 -- sorted lists

	Returns:
	A sorted list containing the unique values in L1 and L2.
	"""
	n1 = len(L1)
	n2 = len(L2)
	i1 = 0  # index into L1
	i2 = 0  # index into L2
	L = []  # output list, starts empty

	# Combine the two sorted lists by appending to L the lesser exposed element of the two lists.
	while i1 < n1 and i2 < n2:
		if L1[i1] < L2[i2]:
			L.append(L1[i1])
			i1 += 1
		elif L1[i1] > L2[i2]:
			L.append(L2[i2])
			i2 += 1
		else:  # duplicates if they are equal
			duplicate = L1[i1]
			L.append(duplicate)  # arbitrarily insert from L1
			# Keep going through the lists, until finding a different number.
			while i1 < n1 and L1[i1] == duplicate:
				i1 += 1
			while i2 < n2 and L2[i2] == duplicate:
				i2 += 1

	# At this point, at least one of the lists is exhausted.  If the other list
	# is not, then copy the remainder onto the end of L.
	if i1 < n1:
		L += L1[i1:]  # append remainder of L1
	if i2 < n2:
		L += L2[i2:]  # append remainder of L2

	return L


# Testing
if __name__ == "__main__":
	print(merge_lists([2, 5, 8], [1, 3, 5, 5]))  # should print [1, 2, 3, 5, 8]

	# Examples from textbook.
	# Exact subset sum.
	print(exact_subset_sum([1, 4, 5], 3, 7))  # should be 6
	print(exact_subset_sum([104, 102, 201, 101], 4, 308))  # should be 307

	# Trim.
	l = [10, 11, 12, 15, 20, 21, 22, 23, 24, 29]
	print(trim(l, 0.1))  # should print [10, 12, 15, 20, 23, 29]

	# Approx subset sum.
	print(approx_subset_sum([104, 102, 201, 101], 4, 308, 0.4))  # should be 302
