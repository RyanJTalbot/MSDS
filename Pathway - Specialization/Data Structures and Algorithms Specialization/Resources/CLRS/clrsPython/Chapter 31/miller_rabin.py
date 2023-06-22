#!/usr/bin/env python3
# miller_rabin.py

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

from random import randint
from modular_exponentiation import modular_exponentiation


def witness(a, n):
	"""Determine whether a is a witness to the compositeness of n.

	Arguments: 
	a -- randomly chosen base value in the range 2 to n-2
	n -- an odd integer greater than 2
	"""
	assert n > 2 and (n % 2 == 1) 	# n must be odd and greater than 2

	# Let t and u be such that t >= 1, u is odd, and n - 1 = (2**t) * u.
	t = 0 	# number of trailing zeros in binary form
	while ((n - 1) >> t) & 1 == 0:  # while more zeros
		t += 1
	u = (n - 1) >> t  # u is the odd integer without trailing zeros

	x_i_minus_1 = modular_exponentiation(a, u, n)  # x_0
	for i in range(1, t + 1):
		x_i = (x_i_minus_1 * x_i_minus_1) % n
		if x_i == 1 and x_i_minus_1 != 1 and x_i_minus_1 != (n - 1):
			return True  # found a nontrivial square root of 1
		x_i_minus_1 = x_i
	# Return true if a^(n - 1) (mod n) is not equal to 1 like pseudoprime
	if x_i != 1:  # the last value computed (x_t in line 7 in textbook)
		return True  # composite, as in pseudoprime
	return False


def miller_rabin(n, s):
	"""Return False if n is composite, True if n is almost surely prime.

	Arguments:
	n -- an odd integer greater than 2 to be tested for primality
	s -- number of random values chosen for a
	"""
	for j in range(s):
		# Probabilistic search for a proof that n is composite.
		a = randint(2, n - 2)
		if witness(a, n):
			return False  # n is definitely composite
	return True  # n is almost surely prime


# Testing
if __name__ == "__main__":

	print(miller_rabin(49979687, 30))		# prime number
	print(miller_rabin(49979685, 30)) 		# composite

	print(miller_rabin(1301081, 40))        # prime number
	print(miller_rabin(130108123, 40)) 		# composite

	# Even n.
	miller_rabin(100235612, 30) 		# assertion error
