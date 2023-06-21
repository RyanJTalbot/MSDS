#!/usr/bin/env python3
# adjacency_list_graph.py

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

from dll_sentinel import DLLSentinel
from adjacency_matrix_graph import AdjacencyMatrixGraph


class Edge:

	def __init__(self, v, weight=None):
		"""Initialize an edge to add to the adjacency list of another vertex.

		Arguments:
		v -- the other vertex that the edge is incident on
		weight -- optional parameter for weighted graphs
		"""
		self.v = v
		if weight is not None:
			self.weight = weight

	def get_v(self):
		"""Return the vertex index."""
		return self.v

	def get_weight(self):
		"""Return the weight of this edge."""
		return self.weight

	def set_weight(self, weight):
		"""Set the weight of this edge."""
		self.weight = weight

	def __str__(self):
		"""String version of the vertex with optional weight in parentheses."""
		return self.strmap(lambda v: v)

	def strmap(self, mapping_func):
		"""String version of the vertex with optional weight in parentheses.
		Vertex numbers are mapped according to a mapping function."""
		string = str(mapping_func(self.v))
		if hasattr(self, "weight"):
			string += " (" + str(self.weight) + ")"
		return string


class AdjacencyListGraph:

	def __init__(self, card_V, directed=True, weighted=False):
		"""Initialize a graph implemented by an adjacency list. Vertices are
		numbered from 0, so that adj_list[i] corresponds to adjacency list of vertex i.

		Arguments:
		card_V -- number of vertices in this graph
		directed -- boolean indicating whether the graph is directed
		weighted -- boolean indicating whether edges are weighted
		"""
		self.directed = directed
		self.weighted = weighted
		self.adj_lists = [None] * card_V
		for i in range(card_V):
			# Each adjacency list is implemented as a linked list.
			self.adj_lists[i] = DLLSentinel(get_key_func=Edge.get_v)  # will be a list of Edge objects
		self.card_V = card_V
		self.card_E = 0

	def get_card_V(self):
		"""Return the number of vertices in this graph."""
		return self.card_V

	def get_card_E(self):
		"""Return the number of edges in this graph."""
		return self.card_E

	def get_adj_lists(self):
		"""Return the adjacency lists of all the vertices in this graph."""
		return self.adj_lists

	def get_adj_list(self, u):
		"""Return an iterator for the adjacency list of vertex u."""
		return self.adj_lists[u].iterator()

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

		# An undirected graph cannot have self-loops.
		if not self.directed and u == v:
			raise RuntimeError("Cannot insert self-loop (" + str(u) + ", " + str(v) + ") into undirected graph")

		# Cannot insert multiple edges between two vertices.
		if self.has_edge(u, v):
			raise RuntimeError("An edge (" + str(u) + ", " + str(v) + ") already exists.")
		self.adj_lists[u].append(Edge(v, weight))
		self.card_E += 1

		# If this graph is undirected, insert an edge from v to u.
		if not self.directed:
			# Cannot insert multiple edges between two vertices.
			if self.has_edge(v, u):
				raise RuntimeError("An edge (" + str(v) + ", " + str(u) + ") already exists.")
			self.adj_lists[v].append(Edge(u, weight))

	def find_edge(self, u, v):
		"""Return the edge object for edge (u, v) if (u, v) is in this graph, None otherwise."""
		edge = self.adj_lists[u].search(v)
		if edge is None:
			return None
		else:
			return edge.data

	def has_edge(self, u, v):
		"""Return True if edge (u, v) is in this graph, False otherwise."""
		return self.find_edge(u, v) is not None

	def delete_edge(self, u, v, delete_undirected=True):
		"""Delete edge (u, v) if it exists.  No error if it does not exist.
			Delete both directions if the graph is undirected and delete_undirected is True."""
		edge = self.adj_lists[u].search(v)
		if edge is not None:
			self.adj_lists[u].delete(edge)
			self.card_E -= 1

		if not self.directed and delete_undirected:
			edge = self.adj_lists[v].search(u)
			if edge is not None:
				self.adj_lists[v].delete(edge)

	def copy(self):
		"""Return a copy of this graph."""
		copy = AdjacencyListGraph(self.card_V, self.directed, self.weighted)
		copy.card_E = self.card_E
		for u in range(self.card_V):
			copy.adj_lists[u] = self.adj_lists[u].copy()
		return copy

	def get_edge_list(self):
		"""Return a Python list containing the edges of this graph."""
		edge_list = []
		for u in range(self.card_V):
			adj_list = self.get_adj_list(u)
			for edge in adj_list:
				v = edge.get_v()
				if self.directed or u < v:
					edge_list.append((u, v))
		return edge_list

	def transpose(self):
		"""Return the transpose of this graph."""
		xpose = AdjacencyListGraph(self.card_V, self.directed, self.weighted)
		for u in range(self.card_V):
			adj_list = self.get_adj_list(u)
			for edge in adj_list:
				v = edge.get_v()
				if self.weighted:
					weight = edge.get_weight()
				else:
					weight = None
				xpose.insert_edge(v, u, weight)
		return xpose

	def adjacency_matrix(self):
		"""Return the adjacency-matrix representation of this graph."""
		card_V = self.get_card_V()
		matrix = AdjacencyMatrixGraph(card_V, self.directed, self.weighted)
		weight_func = lambda edge: edge.get_weight() if self.weighted else None
		for u in range(card_V):
			adj_list = self.get_adj_list(u)
			for edge in adj_list:
				matrix.insert_edge(u, edge.get_v(), weight_func(edge))
		return matrix

	def __str__(self):
		"""Return the adjacency lists formatted as a string."""
		return self.strmap()

	def strmap(self, mapping_func=None):
		"""Return the adjacency lists formatted as a string, but mapping vertex numbers
		by a mapping function.  If mapping_func is None, then do not map."""
		if mapping_func is None:
			mapping_func = lambda i: i

		result = ""
		for i in range(self.card_V):
			result += str(mapping_func(i)) + ": "
			for edge in self.get_adj_list(i):
				result += edge.strmap(mapping_func) + " "
			result += "\n"
		return result


# Testing
if __name__ == "__main__":

	import numpy as np

	# Directed.
	array1 = np.random.randint(10, size=20)
	graph1 = AdjacencyListGraph(10)
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
	graph2 = AdjacencyListGraph(10, directed=False)
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
	graph3 = AdjacencyListGraph(10, True, True)
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

	# Test transpose.
	xpose1 = graph1.transpose()
	print(xpose1)
