#!/usr/bin/env python3
# approx_tsp_tour.py

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

from mst import prim
from dfs import dfs
from math import sqrt 	# for testing


def approx_tsp_tour(G, mapping_func=None, verbose=False):
	"""Find a hamiltonian cycle that gives a lower bound of an optimal
	traveling salesman tour.

	Arguments:
	G -- a complete undirected graph with costs as edge weights
	mapping_func -- a function mapping vertex numbers to strings; if None, then no mapping
	verbose -- boolean indicating whether to print out the minimum spanning tree
	"""
	mst = prim(G, 0)  # root set to first vertex
	if verbose:
		if mapping_func is None:
			mapping_func = lambda i: str(i)
		print(mst.strmap(mapping_func))
	# Depth-first search gives a preorder walk.  Append each vertex when first discovered.
	tour = []
	dfs(mst, discover_func=lambda x: tour.append(x))
	return tour


def compute_dist(p1, p2):
	"""Compute the euclidean distance between two points.

	Arguments:
	p1, p2 -- the points, each an (x, y) tuple

	Returns:
	The euclidean distance between p1 and p2.
	"""
	delta_x = p1[0] - p2[0]
	delta_y = p1[1] - p2[1]
	return sqrt((delta_x * delta_x) + (delta_y * delta_y))


# Testing
if __name__ == "__main__":
	from adjacency_list_graph import AdjacencyListGraph

	# Example from textbook.
	# Form a complete G.  Each tuple gives a vertex name and a tuple with its coordinates.
	vertices = [('a', (1, 4)), ('b', (1, 2)), ('c', (0, 1)), ('d', (3, 4)),
				('e', (4, 3)), ('f', (3, 2)), ('g', (5, 2)), ('h', (2, 0))]
	n = len(vertices)
	graph = AdjacencyListGraph(n, False, True)  # undirected, weighted
	for i in range(n):
		for j in range(i+1, n):
			graph.insert_edge(i, j, compute_dist(vertices[i][1], vertices[j][1]))
	mapping_func = lambda i: vertices[i][0]
	print(graph.strmap(mapping_func))
	tour = approx_tsp_tour(graph, mapping_func, True)  # gives a different tour from the textbook example
	print([vertices[i][0] for i in tour])
	cost = 0  # compute the cost of the tour
	for i in range(n-1):
		cost += graph.find_edge(tour[i], tour[i+1]).get_weight()
	cost += graph.find_edge(tour[0], tour[n-1]).get_weight()
	print(cost)
