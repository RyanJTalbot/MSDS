#!/usr/bin/env python3
# approx_vertex_cover.py

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

# A vertex cover of an undirected graph is a subset of vertices such that if
# (u, v) is an edge of G, then at least one of u and v is in vertex cover.

from adjacency_list_graph import AdjacencyListGraph


def approx_vertex_cover(G):
	"""Find a near-optimal vertex cover of an undirected graph G, no more
	than twice the size of the optimal vertex cover.

	Argument:
	G -- an undirected graph implemented with adjacency lists

	Returns:
	A set of vertices forming the vertex cover.
	"""
	C = set()  # the vertex cover starts out empty
	card_V = G.get_card_V()
	graph_copy = G.copy()

	# Iterate through the remaining edges.
	for u in range(card_V):
		for edge in graph_copy.get_adj_list(u):  # iterates 0 times if u's incident edges are already deleted
			v = edge.get_v()
			C.add(u)
			C.add(v)
			# Delete all edges incident on u or on v.
			delete_edges(graph_copy, u)
			delete_edges(graph_copy, v)
			break
	return C


def delete_edges(G, u):
	"""Delete every edge incident on u in an undirected graph G"""
	# First delete all edges of the form (v, u).
	for edge in G.get_adj_list(u):
		v = edge.get_v()
		G.delete_edge(v, u, False)  # don't delete (u, v) yet

	# Then just delete the entire adjacency list for u.
	G.get_adj_lists()[u].delete_all()


# Testing
if __name__ == "__main__":
	import numpy as np

	# Example from textbook.
	vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	edges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('d', 'e'), ('d', 'f'), ('d', 'g'), ('e', 'f')]
	graph1 = AdjacencyListGraph(len(vertices), False)
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
	print(graph1.strmap(lambda i: vertices[i]))
	C = approx_vertex_cover(graph1)
	print(set([vertices[i] for i in C]))  # gives a different answer from the example in the textbook, with same cardinality
	print()

	# Larger example.
	graph2 = AdjacencyListGraph(50, False)
	for i in range(50):
		for j in range(np.random.randint(5)):
			rand = np.random.randint(50)
			if rand != i:
				try:
					# Ignore multiple edge inserts, keep first one.
					graph2.insert_edge(i, rand)
				except RuntimeError:
					pass
	print(graph2)
	C = approx_vertex_cover(graph2)
	print(C)
