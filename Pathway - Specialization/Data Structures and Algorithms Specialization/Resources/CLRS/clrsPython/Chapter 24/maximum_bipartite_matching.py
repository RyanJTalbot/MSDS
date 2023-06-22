#!/usr/bin/env python3
# maximum_bipartite_matching.py

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

from flow_network import FlowNetwork
from ford_fulkerson import edmonds_karp


def maximum_bipartite_matching(G, left, right):
	"""Find maximum matching between disjoint left and right sides
	of a bipartite graph. A matching is a subset of edges that for 
	for all vertices v, at most one edge is incident on v.

	Arguments:
	G -- a bipartite, undirected graph
	left -- list of indices of vertices on the left
	right -- list of indices of vertices on the right
	"""
	card_V = G.get_card_V()
	# Index of additional vertices. 
	source = card_V
	sink = card_V + 1

	G_prime = FlowNetwork(card_V + 2)
	for u in left:
		# Copy edges over with unit capacity. 
		for edge in G.get_adj_list(u):
			G_prime.insert_edge(u, edge.get_v(), 1)
	# Connect the source and sink vertices. 
	for u in left:
		G_prime.insert_edge(source, u, 1)
	for v in right:
		G_prime.insert_edge(v, sink, 1)

	# Call the Edmonds-Karp algorithm to find a maximum flow.
	edmonds_karp(G_prime, source, sink)

	# Return a list of edges with flow, but from the original graph.
	pairs = []
	for u in left:
		for edge in G_prime.get_adj_list(u):
			v = edge.get_v()
			# Append edges with flow of 1.
			if edge.f == 1 and v < card_V:
				original_edge = edge.original_edge
				graph_edge = G.find_edge(original_edge.get_u(), original_edge.get_v())
				pairs.append(graph_edge)
	return pairs


def print_edges(G, edges, mapping_func=None):
	"""Print the vertices in a set of edges."""
	if mapping_func is None:
		mapping_func = lambda v: v

	for u in range(G.get_card_V()):
		for edge in G.get_adj_list(u):
			if edge in edges:
				print("(" + str(mapping_func(u)) + ", " + str(mapping_func(edge.get_v())) + ")")


def is_matching(G, pairs):
	"""Verify that the pairs form a matching: no vertex has more than one incident edge in the pairs."""

	card_V = G.get_card_V()
	matched = [False] * card_V
	for u in range(card_V):
		for edge in G.get_adj_list(u):
			if edge in pairs:
				v = edge.get_v()
				if matched[u] or matched[v]:
					return False  # vertex already matched
				else:
					matched[u] = True
					matched[v] = True

	return True


# Testing
if __name__ == "__main__":

	from adjacency_list_graph import AdjacencyListGraph

	# Example from textbook.  Even-numbered vertices on left, odd on right.
	# Gives a different maximum matching from the example, but with the same
	# number of edges.
	graph1 = AdjacencyListGraph(9)
	left = {0, 2, 4, 6, 8}
	right = {1, 3, 5, 7}
	graph1.insert_edge(0, 1)
	graph1.insert_edge(2, 1)
	graph1.insert_edge(2, 5)
	graph1.insert_edge(4, 3)
	graph1.insert_edge(4, 5)
	graph1.insert_edge(4, 7)
	graph1.insert_edge(6, 5)
	graph1.insert_edge(8, 5)
	pairs = maximum_bipartite_matching(graph1, left, right)
	print_edges(graph1, pairs)
	print(is_matching(graph1, pairs))
