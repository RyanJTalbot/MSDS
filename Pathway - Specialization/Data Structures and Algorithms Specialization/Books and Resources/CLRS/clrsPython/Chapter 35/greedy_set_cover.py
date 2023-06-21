#!/usr/bin/env python3
# greedy_set_cover.py

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

def greedy_set_cover(X, F):
	"""Find a minimum size subset of F whose members cover all of X.

	Arguments:
	X -- a finite set
	F -- family of subsets of X, such that every element of X belongs
	to at least one subset in F, given as a list

	Returns:
	A subset of F that contains every element in X
	"""
	U = X  # set U contains remaining uncovered elements
	C = []  # list C contains the cover being constructed

	while len(U) > 0:  # while some element is still uncovered
		# Select S in F that maximizes the size of S intersect U.
		S = None
		max_intersection = 0  # maximum intersection size found so far
		for subset in F:
			this_intersection = len(subset & U)
			if this_intersection > max_intersection:
				S = subset
				max_intersection = this_intersection
		U = U - S
		C.append(S)

	return C


# Testing
if __name__ == "__main__":

	# Textbook example; number left to right.
	X = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
	s1 = {1, 2, 3, 4, 5, 6}
	s2 = {5, 6, 8, 9}
	s3 = {1, 4, 7, 10}
	s4 = {2, 5, 7, 8, 11}
	s5 = {3, 6, 9, 12}
	s6 = {10, 11}

	F = [s1, s2, s3, s4, s5, s6]
	C = greedy_set_cover(X, F)  # should be sets s1, s4, s5, s6 or s1, s4, s5, s3
	print(C)
