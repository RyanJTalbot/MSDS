#!/usr/bin/env python3
# activity_selector.py

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

from dll_sentinel import DLLSentinel

# Activities i and j are compatible if s[i] >= f[j] or s[j] >= f[i],
# that is, if their intervals of time do not overlap.


def recursive_activity_selector(s, f, k, n):
	"""Select a maximum subset of mutually compatible activities.

	Arguments:
	s -- array of start times. Activity i has start time s[i]. s[0] must be 0.
	f -- array of finish times. Activity i has finish time f[i], 
	where 0 <= s[i] < f[i] < infinity. f[0] must be 0.
	k -- index of the activity with the first start time in the subproblem
	n -- number of input activities already ordered by monotonically increasing finish time

	Returns:
	Maximum size subset of possible activities represented as a linked list
	"""
	m = k + 1
	while m < n and s[m] < f[k]:  # find the first activity to start after activity k finishes
		m += 1
	if m < n:                     # insert if compatible
		result = recursive_activity_selector(s, f, m, n)
		result.prepend("activity" + str(m))  # each activity is just a string
		return result
	else:
		return DLLSentinel()


def greedy_activity_selector(s, f, n):
	"""Select a maximum subset of mutually compatible activities.

	Arguments:
	s -- array of start times. Activity i has start time s[i]. s[0] must be 0.
	f -- array of finish times. Activity i has finish time f[i], 
	where 0 <= s[i] < f[i] < infinity. f[0] must be 0.
	Assumption:
	Input activities are ordered by monotonically increasing finish time
	Returns:
	a -- maximum size subset of possible activites represented as linked list
	"""
	a = DLLSentinel()
	a.prepend("activity1")
	k = 1
	for m in range(2, n):
		if s[m] >= f[k]:                   # does activity m start after activity k finishes?
			a.append("activity" + str(m))  # yes, so choose it
			k = m                          # and continue from there
	return a


# Testing
if __name__ == "__main__":

	import numpy as np
	from merge_sort import merge_sort

	# Textbook example.
	s = [0, 1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
	f = [0, 4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16]
	# Should be 1, 4, 8, 11
	print(recursive_activity_selector(s, f, 0, len(s)))
	print(greedy_activity_selector(s, f, len(s)))

	s = np.random.randint(1, 100, size=100)
	merge_sort(s)
	s = np.insert(s, 0, 0)  # must start with 0
	f = np.random.randint(1, 100, size=100)
	merge_sort(f)           # must be increasing order
	f = np.insert(f, 0, 0)  # must start with 0
	f += s  # ensure finish time is after start
	print(s)
	print(f)
	print(recursive_activity_selector(s, f, 0, len(s)))
	print(greedy_activity_selector(s, f, len(s)))
