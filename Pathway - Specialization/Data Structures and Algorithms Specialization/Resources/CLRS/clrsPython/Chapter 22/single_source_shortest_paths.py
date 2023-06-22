#!/usr/bin/env python3
# single_source_shortest_paths.py

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

def initialize_single_source(G, s):
	"""Initialize distance and predecessor values for vertices in graph. 

	Arguments:
	G -- a graph
	s -- index of the source vertex for shortest paths
	"""
	# Initialize d and pred.
	card_V = G.get_card_V()
	# d[v] is an upper bound on the weight of a shortest path from source s to v.
	d = [float('inf')] * card_V
	pi = [None] * card_V
	d[s] = 0
	return d, pi


def relax(u, v, w, d, pi, relax_func=None):
	"""Improve the shortest path to v found so far.

	Arguments:
	u, v -- relaxing the edge (u, v))
	w -- weight of the edge (u, v)
	d -- upper bound on the weight of a shortest path from source s to v
	pi -- list of predecessors
	relax_func -- function called after relaxing an edge, default is to do nothing
	"""
	if d[v] > d[u] + w:
		d[v] = d[u] + w  # reduce v's shortest path weight
		pi[v] = u        # update v's predecessor predecessor
		if relax_func is not None:
			relax_func(v)
