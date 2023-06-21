#!/usr/bin/env python3
# strongly_connected_components.py

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

from dfs import dfs
from counting_sort import counting_sort


def strongly_connected_components(G):
	"""Compute the strongly connected components of a directed graph.

	G -- a directed graph, represented by adjacency lists
	start_component_func -- function called to create a depth first tree
	add_to_component -- function called to add vertices to the tree
	"""
	# Throw error if undirected.
	if not G.is_directed():
		raise RuntimeError("Graph must be directed.")
	# Compute finishing times. 
	d, f, pi = dfs(G)
	G_transpose = G.transpose()

	# Create a list of the vertices in order of decreasing finish times.
	card_V = G.get_card_V()
	vertices = [(i, f[i]) for i in range(card_V)]
	sorted_vertices = counting_sort(vertices, card_V, 2*card_V, lambda x: x[1])
	sorted_vertices = [x[0] for x in sorted_vertices[::-1]]  # vertices in order of decreasing finish times

	# Call DFS on the graph transpose, considering vertices in order
	# of decreasing finish times. Upon creating each depth-first tree, start
	# a new component. When discovering a vertex, add it to the component being constructed.
	components = []
	dfs(G_transpose, lambda: components.append([]), lambda u: components[-1].append(u), None, sorted_vertices)
	return components


# Testing
if __name__ == "__main__":
	import numpy as np 
	from adjacency_list_graph import AdjacencyListGraph

	# Directed. 
	array1 = np.arange(10)
	np.random.shuffle(array1)
	graph1 = AdjacencyListGraph(10)
	for i in range(0, len(array1)):
		for j in range(np.random.randint(1, 4)):
			try:
				graph1.insert_edge(i, np.random.randint(10))
			except RuntimeError as e:
				pass
	print(graph1)
	components = strongly_connected_components(graph1)
	print(components)
	print()

	# Textbook example.
	vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	edges = [('a', 'b'), ('b', 'c'), ('b', 'e'), ('b', 'f'), ('c', 'd'), ('c', 'g'),
			 ('d', 'c'), ('d', 'h'), ('e', 'f'), ('e', 'a'), ('f', 'g'), ('g', 'f'),
			 ('g', 'h'), ('h', 'h')]
	graph2 = AdjacencyListGraph(len(vertices))
	for edge in edges:
		graph2.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
	print(graph2.strmap(lambda i: vertices[i]))
	components = strongly_connected_components(graph2)
	for component in components:
		print([vertices[i] for i in component])
