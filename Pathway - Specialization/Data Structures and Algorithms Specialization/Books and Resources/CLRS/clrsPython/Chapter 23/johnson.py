#!/usr/bin/env python3
# johnson.py

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

import numpy as np
from bellman_ford import bellman_ford
from dijkstra import dijkstra


def johnson(G):
	"""Compute all-pairs shortest paths. 

	Argument: 
	G -- a weighted, directed graph represented by adjacency lists

	Returns:
	A matrix of shortest-path weights
	"""
	card_V = G.get_card_V()
	s = card_V 	# index of additional vertex
	# Compute G_prime which is the same as g with with an extra vertex and
	# 0-weight edges from the extra vertex to all other vertices. The extra vertex
	# is the next available index. 
	G_prime = AdjacencyListGraph(card_V + 1, True, True)
	for i in range(card_V):
		G_prime.insert_edge(s, i, 0)  # 0-weight edges from s to all other vertices
		for edge in G.get_adj_list(i):  # copy all other edges
			G_prime.insert_edge(i, edge.get_v(), edge.get_weight())

	bellman_ford_d, pi, no_neg_cycle = bellman_ford(G_prime, s)
	if not no_neg_cycle:  # negative weight cycle?
		print("The input graph contains a negative-weight cycle.")
	else:  # no negative-weight cycle, so proceed
		card_V_prime = G_prime.get_card_V()
		h = bellman_ford_d  # set h(v) to the shortest-path weight from s to v computed by Bellman-Ford

		# Reweight all edges of G_prime to produce nonnegative weights.
		for u in range(card_V_prime):
			for edge in G_prime.get_adj_list(u):
				edge.set_weight(edge.get_weight() + h[u] - h[edge.get_v()])

		# Compute shortest paths from each vertex u with Dijkstra's algorithm.
		d = np.ndarray((card_V, card_V))
		for u in range(card_V):
			dijkstra_d, pi = dijkstra(G_prime, u)
			for v in range(card_V):
				d[u, v] = dijkstra_d[v] + h[v] - h[u]

		return d


# Testing
if __name__ == "__main__":

	from adjacency_list_graph import AdjacencyListGraph
	from all_pairs_shortest_paths import create_W
	from floyd_warshall import floyd_warshall
	from generate_random_graph import generate_random_graph

	# Textbook example
	vertices = [1, 2, 3, 4, 5]
	edges = [(1, 2, 3), (1, 3, 8), (1, 5, -4), (2, 4, 1), (2, 5, 7),
				(3, 2, 4), (4, 1, 2), (4, 3, -5), (5, 4, 6)]
	graph1 = AdjacencyListGraph(len(vertices), True, True)
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])
	print(graph1.strmap(lambda i: vertices[i]))
	johnson_d = johnson(graph1)
	print(johnson_d)
	fw_d = floyd_warshall(create_W(graph1.adjacency_matrix(), len(vertices)), len(vertices))
	print(np.array_equal(johnson_d, fw_d))

	# Larger example.
	n = 50
	graph2 = generate_random_graph(n, 0.05, True, True, True, -2, 20)
	print(graph2)
	johnson_d = johnson(graph2)
	print(johnson_d)
	fw_d = floyd_warshall(create_W(graph2.adjacency_matrix(), n), n)
	print(np.array_equal(johnson_d, fw_d))
