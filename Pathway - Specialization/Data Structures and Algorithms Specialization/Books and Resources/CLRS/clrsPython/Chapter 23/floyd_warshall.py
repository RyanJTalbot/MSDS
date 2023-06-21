#!/usr/bin/env python3
# floyd_warshall.py

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

import numpy as np


def floyd_warshall(W, n):
	"""Compute all-pairs shortest paths. 

	Argument: 
	W -- the weighted adjacency matrix for the graph, but with 0 on the diagonal
	n -- each matrix is n x n

	Returns:
	n x n matrix of shortest-path weights in G

	Note: Implements the Floyd-Warshall' procedure in Exercise 23.2-4
	"""
	d = W.copy()
	for k in range(n):
		for i in range(n):
			for j in range(n):
				d[i,j] = min(d[i,j], d[i,k] + d[k,j])
	return d


def transitive_closure(G, n):
	"""Return the transitive closure of a directed graph. The transitive closure is
	a graph with an edge from i to j if and only if a path exists from i to j.

	Argument:
	G -- a weighted, directed graph represented by an adjacency matrix
	n -- matrices are n x n
	Returns:
	A transitive closure matrix in which the [i][j] entry is True
	if there is a path in G from vertex i to vertex j, False otherwise

	Note: Implements a version of the Transitive-Closure procedure like the
	Floyd-Warshall' procedure in Exercise 23.2-4.
	"""

	t = np.ndarray((n,n), dtype=bool)
	for i in range(n):
		for j in range(n):
			t[i,j] = i == j or G.has_edge(i, j)

	for k in range(n):
		for i in range(n):
			for j in range(n):
				t[i,j] = t[i,j] or (t[i,k] and t[k,j])

	return t


# Testing
if __name__ == "__main__":

	from adjacency_matrix_graph import AdjacencyMatrixGraph
	from all_pairs_shortest_paths import create_W

	# Textbook example for Floyd-Warshall.
	vertices1 = [1, 2, 3, 4, 5]
	n = len(vertices1)
	edges = [(0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 3, 1), (1, 4, 7),
			 (2, 1, 4), (3, 0, 2), (3, 2, -5), (4, 3, 6)]
	graph1 = AdjacencyMatrixGraph(n, True, True)
	for edge in edges:
		graph1.insert_edge(edge[0], edge[1], edge[2])
	print(graph1)
	w = create_W(graph1, n)
	fw_result = floyd_warshall(w, n)
	print(fw_result)

	# Textbook example for transitive closure.
	vertices2 = [1, 2, 3, 4]
	n = len(vertices2)
	edges = [(2, 3), (2, 4), (3, 2), (4, 1), (4, 3)]
	graph2 = AdjacencyMatrixGraph(n, True)
	for edge in edges:
		graph2.insert_edge(vertices2.index(edge[0]), vertices2.index(edge[1]))
	print(graph2)
	tc_result = transitive_closure(graph2, n)
	print(tc_result)
