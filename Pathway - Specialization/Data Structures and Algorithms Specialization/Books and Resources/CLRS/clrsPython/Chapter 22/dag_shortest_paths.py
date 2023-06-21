#!/usr/bin/env python3
# dag_shortest_paths.py

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

from single_source_shortest_paths import initialize_single_source, relax
from topological_sort import topological_sort


def dag_shortest_paths(G, s):
	"""Solve single-source shortest-paths problem on a directed acyclic graph.

	Arguments:
	G -- a directed, weighted graph with no cycles
	s -- index of source vertex
	Returns:
	d -- distances from source s
	pi -- predecessors
	"""
	# Impose linear ordering on the vertices. 
	ordered = topological_sort(G)
	d, pi = initialize_single_source(G, s)
	# Make one pass through vertices in topologically sorted order. 
	for u in ordered.iterator():
		for edge in G.get_adj_list(u):
			# Relax each edge that leaves vertex u.
			relax(u, edge.get_v(), edge.get_weight(), d, pi)
			
	return d, pi


# Testing
if __name__ == "__main__":

	from adjacency_list_graph import AdjacencyListGraph

	# Textbook example. 
	vertices = ['r', 's', 't', 'x', 'y', 'z']
	edges = [('r', 's', 5), ('r', 't', 3), ('s', 't', 2), ('s', 'x', 6), ('t', 'x', 7),
			('t', 'y', 4), ('t', 'z', 2), ('x', 'y', -1), ('y', 'z', -2)]
	graph1 = AdjacencyListGraph(len(vertices), True, True)
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])
	print(graph1.strmap(lambda i: vertices[i]))
	# d should be [inf, 0, 2, 6, 5, 3]
	# pi should be [None, None, s, s, x, y]
	d, pi = dag_shortest_paths(graph1, vertices.index('s'))
	for i in range(len(vertices)):
		print(vertices[i] + ": d = " + str(d[i]) + ", pi = " + ("None" if pi[i] is None else vertices[pi[i]]))
