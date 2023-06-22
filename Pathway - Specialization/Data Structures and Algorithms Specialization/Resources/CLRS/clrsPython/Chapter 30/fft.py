#!/usr/bin/env python3
# fft.py

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

import numpy as np


def fft(a, n):
	"""Compute the discrete Fourier transform of an n-element vector a.

	Argument:
	a -- a numpy array or list representing coefficients of a polynomial
	n -- length of a; MUST be a power of 2
	"""
	# Base case.
	if n == 1:
		return a  # DFT of 1 element is the element itself

	# Recursive case. 
	root = np.exp(2j * np.pi / n)  # compute roots of unity; np.exp is e^(); 2j in numpy is 2*sqrt(-1)
	omega = 1
	a_even = a[::2]  # even coefficients
	a_odd = a[1::2]  # odd coefficients
	y_even = fft(a_even, n // 2)
	y_odd = fft(a_odd, n // 2)
	y = [None] * n

	for k in range(n // 2):
		# Combine results from the recursive DFT.
		# At this point, omega = root^k.
		y[k] = y_even[k] + omega * y_odd[k]
		y[k + (n // 2)] = y_even[k] -  omega * y_odd[k]
		omega *= root 	# update omega so that omega = e^(2i*pi*k / n)

	return y


# Testing
if __name__ == "__main__":
	n = 8
	array1 = [0] * n
	array1[1] = 1
	result1 = fft(array1, n)  # should be 1 time around the unit circle, evenly spaced
	for i in range(n):
		print(i, ':', result1[i], np.exp(2j * np.pi * i / n))  # will see roundoff error
	print()

	n = 32
	array2 = [0] * n
	array2[2] = 1
	result2 = fft(array2, n)  # should be 2 times around the unit circle, evenly spaced
	for i in range(n):
		print(i, ':', result2[i], np.exp(2j * np.pi * 2 * i / n))  # will see roundoff error
