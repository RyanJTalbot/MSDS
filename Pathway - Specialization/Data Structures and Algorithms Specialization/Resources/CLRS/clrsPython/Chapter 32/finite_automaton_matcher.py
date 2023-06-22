#!/usr/bin/env python3
# finite_automaton_matcher.py

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


def finite_automaton_matcher(T, delta, n, m):
	"""Find all the occurrences of a pattern in the text T.  The pattern
	is implicitly given in the transition function delta.

	Arguments:
	T -- the text
	delta -- transition function
	n -- length of T
	m -- length of the pattern
	"""
	q = 0  # start in state 0
	for i in range(n):
		q = delta[q][T[i]]  # go to next state, based on current state and next character of T
		if q == m:  # match!
			print("Pattern occurs with shift", i - m + 1)  # +1 due to 0-origin indexing


def compute_transition_function(P, sigma, m):
	"""Compute the transition function for a pattern.

	Arguments:
	P -- the pattern
	sigma -- a set of symbols that appear in the pattern
	m -- length of P

	Returns:
	delta -- the transition function, where if the automaton is in state q after reading
	the first i characters of a text T, then delta[q][a] is the length of the
	longest prefix of P that is also a suffix of T[:i].
	"""
	# Initialize a list of dictionaries mapping each character to 0.
	# Indices into the list are state numbers, and indices into the dictionaries are characters.
	delta = [{ch: 0 for ch in sigma} for i in range(m + 1)]

	# Consider all states and all characters.
	for q in range(m + 1):
		for a in sigma:
			k = min(m, q + 1) 	# max possible k
			# While P[:k] is not a suffix of P[:q]a, decrement k.
			# If k reaches 0, stop because P[:k] is the empty string, which is always a suffix.
			while k > 0 and P[:k] != (P[:q] + a)[-k:]:
				k -= 1
			delta[q][a] = k

	return delta


def fa_matcher(T, P, n, m, sigma=None):
	"""Combine compute_transition_function and finite_automaton_matcher.

	Arguments:
	T -- the text
	P -- the pattern
	n -- length of T
	m -- length of P
	sigma -- a set of symbols that appear in the pattern; if None, then
	just the unique characters that appear in T
	"""
	if sigma is None:
		sigma = set(T)  # default alphabet is just the unique characters of T
	delta = compute_transition_function(P, sigma, m)
	finite_automaton_matcher(T, delta, n, m)


# Testing
if __name__ == "__main__":

	T = "ababacbababacababacaba"
	P = "ababaca"
	fa_matcher(T, P, len(T), len(P))  # 2 matches, at shifts 7 and 13
	print()

	T = "acaabc" 
	P = "aab"
	fa_matcher(T, P, len(T), len(P), {'a', 'b', 'c'})  # shift 2
	print()

	T = "2359023141526739921"
	P = "31415"
	fa_matcher(T, P, len(T), len(P))  # shift 6
	print()

	T = "ACCCGTAGACGAGATATATAGGGGACGGGATAAGGCCTAGCGGATCGGATC" + \
		"CGATTACGGCGCGATGCTGACGTACGTACGTACGCGATCGCTTTCGAACGTACGATCACGCATACGACGCA" + \
		"ACGACGATCGATCGGAGGGAAACCCCCCGTTTTAAAGCGCGCTAAAAGCTATGCAGCATCGACTACGAC"
	P = "CGTACGCGATCGCTTTCGAAC"
	fa_matcher(T, P, len(T), len(P), {'A', 'C', 'G', 'T'})  # shift 79
	print()

	# 4 matches, at shifts 6, 73, 89, and 257.
	T = "9765859868653640987087465254327658768760808769758753643254" + \
		"3876876076876989868653640987087986865364098708798769876987685476548" + \
		"736543543654365436543654387609870875764354216545976987947657698769" + \
		"543654376598760987976486508870876087697860876987698769876987698769" + \
		"9868653640987087"
	P = "9868653640987087"
	fa_matcher(T, P, len(T), len(P), set([str(i) for i in range(10)]))
