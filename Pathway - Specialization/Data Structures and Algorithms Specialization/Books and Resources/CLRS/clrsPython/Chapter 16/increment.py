#!/usr/bin/env python3
# increment.py

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

def increment(A, k):
	"""Implement a k-bit binary counter that counts upward from 0. 

	Argument:
	A -- array of bits where A[0] is the lowest-order bit
	k -- number of bits
	"""
	i = 0 
	while i < k and A[i] == 1:
		A[i] = 0  # value of 1 increments to 0
		i += 1
	if i < k:
		A[i] = 1  # carry over 1 to next position


def print_array_binary(A):
	"""Print the array as binary with the right as the lowest-order bit."""
	for i in range(len(A) - 1, -1, -1):
		print(A[i], end="")
	print()


# Testing
if __name__ == "__main__":

	# Increment binary counter.
	k = 8
	A = [0] * k
	for i in range(16):
		increment(A, k)
		print_array_binary(A)

	print()

	B = [0] * k
	for i in range(1 << k):
		increment(B, k)
		print_array_binary(B)  # last array becomes 00000000 because of overflow
