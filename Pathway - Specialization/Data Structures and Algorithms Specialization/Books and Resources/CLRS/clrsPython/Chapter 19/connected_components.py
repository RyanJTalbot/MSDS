#!/usr/bin/env python3
# connected_components.py

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

# Either of the following import statements works.
# from disjoint_set_list import make_set, find_set, union
from disjoint_set_forest import make_set, find_set, union


def connected_components(G):
	"""Compute tge connected components of graph G.

	G -- an undirected graph implemented with adjacency lists
	"""
	card_V = G.get_card_V()
	nodes = [None] * card_V

	# Make a singleton set for each vertex.
	for u in range(card_V):
		nodes[u] = make_set(u)

	# For each edge, unite its endpoint vertices.
	for u in range(card_V):
		for edge in G.get_adj_list(u):
			v = edge.get_v()
			if find_set(nodes[u]) != find_set(nodes[v]):
				union(nodes[u], nodes[v])

	# Two vertices are in the same connected connected component if and only if
	# their corresponding objects are in the same set.
	return nodes


def same_component(u, v, sets):
	"""Return a boolean indicating whether two vertices are in the same connected component.

	Arguments:
	u, v -- indices of distinct vertices
	sets -- list of nodes for the vertices
	"""
	return find_set(sets[u]) == find_set(sets[v])


# Testing
if __name__ == "__main__":

	from adjacency_list_graph import AdjacencyListGraph

	# Textbook example.
	vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
	edges = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd'), ('e', 'f'), ('f', 'g'), ('h', 'i')]
	graph1 = AdjacencyListGraph(len(vertices), False)  # undirected
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
	print(graph1.strmap(lambda i: vertices[i]))

	sets = connected_components(graph1)
	for component in sets:
		print(vertices[int(str(component))], ':', vertices[int(str(find_set(component)))])

	if same_component(vertices.index('a'), vertices.index('c'), sets):
		print('a and c are in the same component')
	else:
		print('a and c are not in the same component')

	if same_component(vertices.index('a'), vertices.index('e'), sets):
		print('a and e are in the same component')
	else:
		print('a and e are not in the same component')
