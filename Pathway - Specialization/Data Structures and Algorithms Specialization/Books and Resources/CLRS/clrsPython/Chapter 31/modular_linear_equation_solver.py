#!/usr/bin/env python3
# modular_linear_equation_solver.py

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

from extended_euclid import extended_euclid


def modular_linear_equation_solver(a, b, n):
	"""Solve ax = b (mod n).

	Assumptions:
	a > 0, n > 0, b is any integer.
	"""
	# Compute d = gcd(a, n).
	# d = a * x_prime + n * y_prime.
	d, x_prime, y_prime = extended_euclid(a, n)
	if b % d == 0:  # does d divide b?
		# Compute solution to ax = b (mod n).
		x_0 = (x_prime * (b // d)) % n
		# Given one solution, x_0, adding multiples of (n/d) % n yields the other d-1 solutions.
		for i in range(d):
			print((x_0 + i * (n//d)) % n, end=" ")
		print()
	else:
		print("No solutions.")


# Testing
if __name__ == "__main__":

	modular_linear_equation_solver(14, 30, 100)  # solutions are 95, 45
	print(95 * 14 % 100 == 30)
	print(45 * 14 % 100 == 30)

	modular_linear_equation_solver(17, 18, 203)  # solution is 13
	print(13 * 17 % 203 == 18)

	modular_linear_equation_solver(5, 7, 30)  # no solution
