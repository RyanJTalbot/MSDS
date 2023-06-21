#!/usr/bin/env python3
# rsa.py

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

from random import randint
from pseudoprime import pseudoprime
from extended_euclid import extended_euclid


def generate_prime(d):
	"""Generate a prime that is d bits long."""
	while True:
		p = randint(1 << (d - 1), (1 << d) - 1) | 1  # generate an odd d-bit number
		if pseudoprime(p): 	# is it is very likely prime?
			return p


def compute_e_d(r):
	"""Compute e and d as the public and secret keys. 

	Argument:
	r -- (p - 1)(q - 1) computed from rsa
	Returns
	e -- small odd integer that is relatively prime to r
	d -- multiplicative inverse of e, mod r. 
	"""
	# Starting from 5, try odd integers until finding one that is relatively prime to r.
	e = 5 		
	while True:
		g, i, j = extended_euclid(r, e)
		if g == 1:
			# e is relatively prime to r. The value of j returned by 
			# euclid, taken mod r, is e's multiplicative inverse, mod r. 
			return e, j % r
		else:
			e += 2


def rsa(d):
	"""Create a pair of public and secret keys from prime numbers. 

	Argument:
	n -- number of bits of prime numbers used

	Returns:
	A pair of public and secret keys, each of which contains two numbers.
	The first is the public key (e, n), and the second is the secret key (d, n).
	"""
	p = generate_prime(d)
	q = generate_prime(d)
	while p == q:  # cannot be equal
		q = generate_prime(d)
		print(q)

	n = p * q
	r = (p-1) * (q-1)
	# Select a small integer e that is relatively prime to r and let d be its multiplication inverse, modulo r.
	e, d = compute_e_d(r)
	return (e, n), (d, n) 	# public key, secret key


# Testing
if __name__ == "__main__":

	public, secret = rsa(100)
	print(public)
	print(secret)
	