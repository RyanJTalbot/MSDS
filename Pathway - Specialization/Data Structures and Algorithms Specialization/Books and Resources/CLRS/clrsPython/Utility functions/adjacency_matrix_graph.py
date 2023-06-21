#!/usr/bin/env python3
# adjacency_matrix_graph.py

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


class AdjacencyMatrixGraph:

	def __init__(self, card_V, directed=True, weighted=False):
		"""Initialize a graph implemented by an adjacency matrix. 

		Arguments:
		card_V -- number of vertices in this graph
		directed -- boolean whether or not graph is directed
		weighted -- boolean whether or not edges are weighted
		"""
		self.directed = directed
		if weighted:
			# For weighted graphs, adj_matrix will default to infinity for no edge.
			self.adj_matrix = np.ndarray((card_V, card_V))
			self.no_edge = float('inf')
			self.adj_matrix.fill(self.no_edge)
		else:
			# For unweighted graphs, adj_matrix will default to 0 for no edge.
			self.adj_matrix = np.zeros(shape=(card_V, card_V), dtype=int)
			self.no_edge = 0
		self.card_V = card_V
		self.weighted = weighted
		self.card_E = 0

	def get_card_V(self):
		"""Return the number of vertices in this graph."""
		return self.card_V

	def get_card_E(self):
		"""Return the number of edges in this graph."""
		return self.card_E

	def get_adj_matrix(self):
		"""Return the adjacency matrix for this graph."""
		return self.adj_matrix

	def is_directed(self):
		"""Return a boolean indicating whether this graph is directed."""
		return self.directed

	def is_weighted(self):
		"""Return a boolean indicating whether this graph is weighted."""
		return self.weighted

	def insert_edge(self, u, v, weight=None):
		"""Insert an edge between vertices u and v.

		Arguments:
		u -- index of vertex u
		v -- index of vertex v
		"""
		# Check whether a weight is missing, or whether a weight is given in an unweighted graph.
		if self.weighted:
			if weight is None:
				raise RuntimeError("Inserting unweighted edge (" + str(u) + ", " + str(v) + ") in weighted graph.")
		else:  # unweighted
			if weight is not None:
				raise RuntimeError("Inserting weighted edge (" + str(u) + ", " + str(v) + ") in unweighted graph.")
			weight = 1  # to indicate the presence of the edge

		# An undirected graph cannot have self-loops.
		if not self.directed and u == v:
			raise RuntimeError("Cannot insert self-loop (" + str(u) + ", " + str(v) + ") into undirected graph")

		# Cannot insert multiple edges between two vertices.
		if self.has_edge(u, v):
			raise RuntimeError("An edge (" + str(u) + ", " + str(v) + ") already exists.")
		self.adj_matrix[u, v] = weight
		self.card_E += 1

		# If undirected, insert edge from v to u.
		if not self.directed:
			if self.has_edge(v, u):
				raise RuntimeError("An edge (" + str(v) + ", " + str(u) + ") already exists.")
			self.adj_matrix[v, u] = weight

	def has_edge(self, u, v):
		"""Return True if edge (u, v) is in this graph, False otherwise."""
		return self.adj_matrix[u, v] != self.no_edge

	def delete_edge(self, u, v, delete_undirected=True):
		"""Delete edge (u, v) if it exists.  No error if it does not exist.
			Delete both directions if the graph is undirected and delete_undirected is True."""
		if self.adj_matrix[u, v] != self.no_edge:
			self.adj_matrix[u, v] = self.no_edge
			self.card_E -= 1
		if not self.directed and delete_undirected:
			self.adj_matrix[v, u] = self.no_edge

	def copy(self):
		"""Return a copy of this graph."""
		c = AdjacencyMatrixGraph(self.card_V, self.directed, self.weighted)
		c.adj_matrix = self.adj_matrix.copy()  # deep copy
		c.card_E = self.card_E
		return c

	def get_edge_list(self):
		"""Return a Python list containing the edges of this graph."""
		edge_list = []
		for u in range(self.card_V):
			if self.directed:
				lowest_v = 0
			else:
				lowest_v = u + 1
			for v in range(lowest_v, self.card_V):
				if self.adj_matrix[u, v] != self.no_edge:
					edge_list.append((u, v))
		return edge_list

	def __str__(self):
		"""Return the adjacency matrix."""
		return str(self.adj_matrix)


# Testing
if __name__ == "__main__":

	import numpy as np

	# Directed.
	array1 = np.random.randint(10, size=20)
	graph1 = AdjacencyMatrixGraph(10)
	for i in range(0, len(array1) - 1, 2):
		try:
			graph1.insert_edge(array1[i], array1[i + 1])
		except RuntimeError as e:
			print(e)
	print(graph1)
	print(graph1.get_card_E())

	# Test get_edge_list.
	print(graph1.get_edge_list())

	# Undirected.
	graph2 = AdjacencyMatrixGraph(10, directed=False)
	for i in range(0, len(array1) - 1, 2):
		try:
			graph2.insert_edge(array1[i], array1[i + 1])
		except RuntimeError as e:
			print(e)
	print(graph2)
	print(graph2.get_card_E())

	# Test get_edge_list.
	print(graph2.get_edge_list())

	# Test has_edge.
	for u in range(graph2.get_card_V()):
		for v in range(graph2.get_card_V()):
			if graph2.has_edge(u, v):
				print("(" + str(u) + ", " + str(v) + ")")
			elif u != v:
				missing_edge = (u, v)
	print("")

	# Test copy.
	graph3 = graph2.copy()
	# Verify that it is a copy by inserting an edge that isn't there yet.
	graph3.insert_edge(*missing_edge)
	print(graph2)
	print(graph3)
	print(graph3.get_card_E())

	# Now delete that edge.
	graph3.delete_edge(*missing_edge)          # delete some edge (u, v)
	graph3.delete_edge(*(missing_edge[::-1]))  # and delete (v, u)
	print(graph3)
	print(graph3.get_card_E())

	# Inserting weighted and unweighted.
	graph3 = AdjacencyMatrixGraph(10, True, True)
	try:  # insert unweighted into weighted
		graph3.insert_edge(0, 1)
	except RuntimeError as e:
		print(e)
	for i in range(0, len(array1) - 1, 2):
		try:
			graph3.insert_edge(array1[i], array1[i + 1], array1[i])
		except RuntimeError as e:
			print(e)
	print(graph3)
	print(graph3.get_card_E())

	# Test get_edge_list.
	print(graph3.get_edge_list())
