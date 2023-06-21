#!/usr/bin/env python3
# extended_euclid.py

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

def extended_euclid(a, b):
	"""Find the greatest common divisor of a and b. 

	Arguments:
	a -- nonnegative integer
	b -- nonnegative integer

	Returns:
	d, x, y such that d = gcd(a, b) = ax + by
	"""
	if b == 0:
		return a, 1, 0  # gcd is a
	else:
		d_prime, x_prime, y_prime = extended_euclid(b, a % b)
		d, x, y = (d_prime, y_prime, x_prime - (a // b) * y_prime)
		return d, x, y


# Testing
if __name__ == "__main__":
	d, x, y = extended_euclid(99, 78)
	print(d, x, y) 	# should be 3, -11, 14

	d, x, y = extended_euclid(1026, 1357)
	print(d, x, y)
	print(1026 * x + 1357 * y == d)
