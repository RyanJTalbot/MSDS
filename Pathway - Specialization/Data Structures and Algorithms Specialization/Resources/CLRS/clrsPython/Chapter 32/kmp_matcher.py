#!/usr/bin/env python3
# kmp_matcher.py

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


def kmp_matcher(T, P, n, m):
	"""Find all the occurrences of the pattern P in the text T.

	Arguments:
	T-- the text
	P -- the pattern
	n -- length of T
	m -- length of P
	"""
	pi = compute_prefix_function(P, m)
	m -= 1  # adjust for 0-origin indexing.
	q = -1  # index in P of last character matched
	for i in range(n):  # scan the text from left to right
		while q > -1 and P[q + 1] != T[i]:  # again, adjust q for 0-origin indexing
			q = pi[q]  # next character does not match
		if P[q + 1] == T[i]:
			q += 1  # next character matches
		if q == m:  # is all of P matched?
			print("Pattern occurs with shift", i - m)
			q = pi[q]  # look for the next match


def compute_prefix_function(P, m):
	"""Encapsulate knowledge about how the pattern matches against shifts of itself.
	We want the longest proper prefix P that is also a proper suffix of P[:q].

	Argument:
	P -- the pattern
	m -- length of P

	Returns:
	pi -- prefix function where pi[q] is the length of the longest prefix
	of P that is a proper suffix of P[:q]
	"""
	pi = [None] * m
	pi[0] = -1  # adjust for 0-origin indexing
	k = -1  # also for 0-origin indexing

	# Match P against itself.
	for q in range(1, m):  # scan P from left to right
		while k > -1 and P[k + 1] != P[q]:  # adjust for 0-origin indexing
			k = pi[k]  # character does not match
		if P[k + 1] == P[q]:
			k += 1  # character matches, continue
		pi[q] = k  # assign prefix to position of last character matched
	return pi


# Testing
if __name__ == "__main__":

	T = "ababacbababacababacaba"
	P = "ababaca"
	kmp_matcher(T, P, len(T), len(P))  # 2 matches, at shifts 7 and 13
	print()

	T = "acaabc"
	P = "aab"
	kmp_matcher(T, P, len(T), len(P))  # shift 2
	print()

	T = "2359023141526739921"
	P = "31415"
	kmp_matcher(T, P, len(T), len(P))  # shift 6
	print()

	T = "ACCCGTAGACGAGATATATAGGGGACGGGATAAGGCCTAGCGGATCGGATC" + \
		"CGATTACGGCGCGATGCTGACGTACGTACGTACGCGATCGCTTTCGAACGTACGATCACGCATACGACGCA" + \
		"ACGACGATCGATCGGAGGGAAACCCCCCGTTTTAAAGCGCGCTAAAAGCTATGCAGCATCGACTACGAC"
	P = "CGTACGCGATCGCTTTCGAAC"
	kmp_matcher(T, P, len(T), len(P))  # shift 79
	print()

	# 4 matches, at shifts 6, 73, 89, and 257.
	T = "9765859868653640987087465254327658768760808769758753643254" + \
		"3876876076876989868653640987087986865364098708798769876987685476548" + \
		"736543543654365436543654387609870875764354216545976987947657698769" + \
		"543654376598760987976486508870876087697860876987698769876987698769" + \
		"9868653640987087"
	P = "9868653640987087"
	kmp_matcher(T, P, len(T), len(P))
