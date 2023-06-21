#!/usr/bin/env python3
# naive_string_matcher.py

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

def naive_string_matcher(T, P, n, m):
	"""Find all the occurrences of the pattern P in the text T.

	Arguments:
	T -- the text
	P -- the pattern
	n -- length of T
	m -- length of P
	"""
	for s in range(n - m + 1): 	# shift over one by one
		if P == T[s: s + m]: 	# compare P to each substring of T with length m
			print("Pattern occurs with shift", s)


# Testing
if __name__ == "__main__":

	T = "acaabc"
	P = "aab"
	naive_string_matcher(T, P, len(T), len(P))
	print()

	T = "ACCCGTAGACGAGATATATAGGGGACGGGATAAGGCCTAGCGGATCGGATC" + \
		"CGATTACGGCGCGATGCTGACGTACGTACGTACGCGATCGCTTTCGAACGTACGATCACGCATACGACGCA" + \
		"ACGACGATCGATCGGAGGGAAACCCCCCGTTTTAAAGCGCGCTAAAAGCTATGCAGCATCGACTACGAC"
	P = "CGTACGCGATCGCTTTCGAAC"
	naive_string_matcher(T, P, len(T), len(P))
	print()

	# 4 matches.
	T = "9765859868653640987087465254327658768760808769758753643254" + \
		"3876876076876989868653640987087986865364098708798769876987685476548" + \
		"736543543654365436543654387609870875764354216545976987947657698769" + \
		"543654376598760987976486508870876087697860876987698769876987698769" + \
		"9868653640987087"
	P = "9868653640987087"
	naive_string_matcher(T, P, len(T), len(P))
