#!/usr/bin/env python3
# bellman_ford.py

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


def bellman_ford(G, s):
	"""Solve the single-source shortest-paths problem in the general case in which
	edge weights may be negative. 

	Arguments:
	G -- a directed, weighted graph
	s -- index of the source vertex
	Returns:
	d -- distances from source s
	pi -- predecessors
	A boolean value indicating whether there is a negative-weight cycle
	reachable from the source; True if no negative-weight cycle, False if there is one
	"""
	card_V = G.get_card_V()
	d, pi = initialize_single_source(G, s)

	# Run through all the edges |V| - 1 times.
	for i in range(1, card_V):
		for u in range(card_V):
			for edge in G.get_adj_list(u):
				# Relax each edge.
				relax(u, edge.get_v(), edge.get_weight(), d, pi)

	# One more pass to see whether a relaxation would have changed a distance.
	for u in range(card_V):
		for edge in G.get_adj_list(u):
			# If changed, a negative cycle exists.
			if d[edge.get_v()] > d[u] + edge.get_weight():
				return d, pi, False  # negative-weight cycle
	return d, pi, True


# Testing
if __name__ == "__main__":

	from adjacency_list_graph import AdjacencyListGraph

	# Textbook example. 
	vertices = ['s', 't', 'x', 'y', 'z']
	edges = [('s', 't', 6), ('s', 'y', 7), ('t', 'x', 5), ('t', 'y', 8), ('t', 'z', -4),
			 ('x', 't', -2), ('y', 'x', -3), ('y', 'z', 9), ('z', 's', 2), ('z', 'x', 7)]
	graph1 = AdjacencyListGraph(len(vertices), True, True)
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])
	print(graph1.strmap(lambda i: vertices[i]))
	# d should be [0, 2, 4, 7, -2], pi should be [None, x, y, s, t]
	d, pi, cycle = bellman_ford(graph1, vertices.index('s'))
	print("No negative-weight cycle:", cycle)
	for i in range(len(vertices)):
		print(vertices[i] + ": d = " + str(d[i]) + ", pi = " + ("None" if pi[i] is None else vertices[pi[i]]))
	print()

	# Negative-weight cycle.
	graph2 = graph1.copy()
	graph2.insert_edge(vertices.index('s'), vertices.index('x'), -5)
	print(graph2.strmap(lambda i: vertices[i]))
	d, pi, cycle = bellman_ford(graph2, vertices.index('s'))
	print("No negative-weight cycle:", cycle)
	for i in range(len(vertices)):
		print(vertices[i] + ": d = " + str(d[i]) + ", pi = " + ("None" if pi[i] is None else vertices[pi[i]]))
