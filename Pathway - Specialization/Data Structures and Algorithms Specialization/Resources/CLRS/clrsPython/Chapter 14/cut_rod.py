#!/usr/bin/env python3
# cut_rod.py

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

# Given a rod of length n and a table of prices for lengths 1, 2, ..., n,
# determine the maximum revenue by cutting up the rod and selling the pieces.


def cut_rod(p, n):
	"""Recursive top-down implementation of cut_rod.

	Arguments:
	p -- list/array of prices where p[0] = 0 and p[i] is the price of a rod of length i
	n -- length of rod

	Returns:
	Maximum revenue from cutting up and selling rod
	"""
	if n == 0:		# Base case. 
		return 0
	q = float('-inf')
	for i in range(1, n + 1):
		q = max(q, p[i] + cut_rod(p, (n - i)))
	return q


def memoized_cut_rod(p, n):
	"""Recursive top-down with memoization implementation of cut_rod.

	Arguments:
	p -- list/array of prices where p[0] = 0 and p[i] is the price of a rod of length i
	n -- length of rod

	Returns:
	Maximum revenue from cutting up and selling rod
	"""
	# r is a list of revenues where r[i] is the maximum revenue for selling a rod of length i, and r[0] = 0.
	r = [float('-inf')] * (n + 1)
	return memoized_cut_rod_aux(p, n, r)


def memoized_cut_rod_aux(p, n, r):
	"""Memoized version of cut_rod.

	Arguments:
	p -- list/array of prices where p[0] = 0 and p[i] is the price of a rod of length i
	n -- length of rod
	r -- list of revenues where r[i] is the maximum revenue for selling a rod of length i, and r[0] = 0

	Returns:
	Maximum revenue from cutting up and selling rod 
	"""
	if r[n] >= 0:  # already have a solution for length n?
		return r[n]
	# Compute q like in cut_rod. 
	if n == 0:
		q = 0
	else:
		q = float('-inf')
		for i in range(1, n + 1):  # i is the position of the first cut
			q = max(q, p[i] + memoized_cut_rod_aux(p, n - i, r))
	r[n] = q  # remember the solution value for length n
	return q


def bottom_up_cut_rod(p, n):
	"""Bottom-up implementation of cut_rod.

	Arguments:
	p -- list/array of prices where p[0] = 0 and p[i] is the price of a rod of length i
	n -- length of rod

	Returns:
	Maximum revenue from cutting up and selling rod
	"""
	r = [None] * (n + 1)  # will remember solution values in r
	r[0] = 0

	for j in range(1, n + 1):  # for increasing rod length j
		q = float('-inf')
		for i in range(1, j + 1):  # i is the position of the first cut
			q = max(q, p[i] + r[j - i])
		r[j] = q  # remember the solution value for length j
	return r[n]


def extended_bottom_up_cut_rod(p, n):
	"""Compute maximum revenue and optimal size of first piece cut off. 

	Arguments:
	p -- list/array of prices where p[0] = 0 and p[i] is the price of a rod of length i
	n -- length of rod

	Returns:
	r -- list of revenues where r[i] is the maximum revenue for selling a rod of length i, and r[0] = 0
	s -- list of sizes where s[i] is the optimal size of the first piece cut off of rod size i with s[0] not being used
	"""
	# Initialize array of revenues and optimal sizes. 
	r = [None] * (n + 1)
	r[0] = 0
	s = [None] * (n + 1)

	for j in range(1, n + 1):  # for increasing rod length j
		q = float('-inf')
		for i in range(1, j + 1):  # i is the position of the first cut
			if q < p[i] + r[j - i]:
				q = p[i] + r[j - i]
				s[j] = i  # best cut location so far for length j
		r[j] = q  # remember the solution value for length j
	return r, s


def print_cut_rod_solution(p, n):
	"""Print how far apart to cut."""
	r, s = extended_bottom_up_cut_rod(p, n)
	while n > 0:
		print(s[n], end=" ")  # cut location for length n
		n -= s[n]  # length of the remainder of the rod
	print()


# Testing
if __name__ == "__main__":

	import numpy as np

	# Textbook example. 
	prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
	# Standard cut rod. 
	print(cut_rod(prices, 4))   # should be 10
	print(cut_rod(prices, 10))  # should be 30
	# Memoized cut rod. 
	print(memoized_cut_rod(prices, 4))   # should be 10
	print(memoized_cut_rod(prices, 10))  # should be 30
	# Bottom up cut rod.
	print(bottom_up_cut_rod(prices, 4))   # should be 10
	print(bottom_up_cut_rod(prices, 10))  # should be 30
	# Extended bottom up cut rod. 
	print_cut_rod_solution(prices, 4)   # should be 2, 2
	print_cut_rod_solution(prices, 10)  # should be 10
	print()
	r, s = extended_bottom_up_cut_rod(prices, 10)
	print(r)
	print(s)
	print()

	# Larger example. 
	prices = np.random.randint(1, 40, size=30)
	prices = np.unique(prices)       # sorted, unique prices
	prices = np.append([0], prices)  # for length 0
	print(prices)

	# Standard cut rod. 
	print(cut_rod(prices, 18))	
	print(cut_rod(prices, 10))	
	# Memoized cut rod. 
	print(memoized_cut_rod(prices, 18))
	print(memoized_cut_rod(prices, 10))
	# Bottom up cut rod.
	print(bottom_up_cut_rod(prices, 18))
	print(bottom_up_cut_rod(prices, 10)) 
	# Extended bottom up cut rod. 
	print_cut_rod_solution(prices, 18)
	print_cut_rod_solution(prices, 10)
