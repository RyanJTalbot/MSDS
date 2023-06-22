#!/usr/bin/env python3
# all_pairs_shortest_paths.py

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


def extend_shortest_paths(L_r_minus_1, W, L_r, n):
	"""Extend the shortest paths given in one matrix by the edge
	weights given in another matrix.

	Arguments:
	L_r_minus_1 -- matrix of shortest-path weights with at most r-1 edges
	W -- matrix or numpy array of edge weights
	L_r -- matrix assumed to be initialized with infinity in all locations--
	at conclusion, holds shortest-path weights with at most r edges
	n -- each matrix is n x n
	"""
	for i in range(n):
		for j in range(n):
			for k in range(n):
				L_r[i, j] = min(L_r[i, j], L_r_minus_1[i, k] + W[k, j])


def slow_apsp(W, L_0, n):
	"""Compute all-pairs shortest paths for a weighted directed graph.

	Arguments:
	L_0 -- a matrix initialized with 0 on the diagonal and infinity everywhere else
	W -- the weighted adjacency matrix for the graph, but with 0 on the diagonal
	n -- each matrix is n x n
	Returns:
	L -- matrix of shortest-path weights, where L[i,j] is the weight of a
	shortest path from vertex i to vertex j
	"""
	L = np.copy(L_0)
	m = np.ndarray((n, n))

	for r in range(1, n):
		m.fill(float('inf'))  # initialize m
		extend_shortest_paths(L, W, m, n)
		L = m.copy()
	return L


def faster_apsp(W, n):
	"""Compute all-pairs shortest paths for a weighted directed graph.

	Arguments:
	W -- the weighted adjacency matrix for the graph, but with 0 on the diagonal
	n -- each matrix is n x n
	Returns:
	L -- matrix of shortest-path weights, where L[i,j] is the weight of a
	shortest path from vertex i to vertex j
	"""
	L = W.copy()
	M = np.ndarray((n,n))
	r = 1
	while r < n-1:
		M.fill(float('inf'))  # initialize M
		extend_shortest_paths(L, L, M, n)  # compute M = L^2
		r *= 2
		L = M.copy()
	return L


def initialize_L_0(n):
	"""Create and return the L_0 matrix, with 0 on the diagonal and infinity everywhere else."""
	L_0 = np.ndarray((n,n))
	L_0.fill(float('inf'))
	for i in range(n):
		L_0[i,i] = 0
	return L_0


def create_W(G, n):
	"""Create and return the W matrix, given an n-vertex graph G represented by an adjacency matrix."""
	W = G.get_adj_matrix().copy()
	for i in range(n):
		W[i,i] = 0
	return W


# Testing
if __name__ == "__main__":

	from adjacency_matrix_graph import AdjacencyMatrixGraph
	from generate_random_graph import generate_random_graph

	# Textbook example.
	vertices = [1, 2, 3, 4, 5]
	n = len(vertices)
	edges = [(0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 3, 1), (1, 4, 7),
			 (2, 1, 4), (3, 0, 2), (3, 2, -5), (4, 3, 6)]
	graph1 = AdjacencyMatrixGraph(len(vertices), True, True)
	for edge in edges:
		graph1.insert_edge(edge[0], edge[1], edge[2])
	print(graph1)
	W = create_W(graph1, n)
	L_0 = initialize_L_0(n)
	slow_L = slow_apsp(W, L_0, n)
	print(slow_L)
	faster_L = faster_apsp(W, n)
	print(faster_L)
	print(np.array_equal(slow_L, faster_L))
	print()

	# Larger example.
	n = 50
	graph2 = generate_random_graph(n, 0.12, False, True, True, 0, 12)
	print(graph2)
	W = create_W(graph2, n)
	# Should be the same.
	L_0 = initialize_L_0(n)
	slow_L = slow_apsp(W, L_0, n)
	print(slow_L)
	faster_L = faster_apsp(W, n)
	print(faster_L)
	print(np.array_equal(slow_L, faster_L))
