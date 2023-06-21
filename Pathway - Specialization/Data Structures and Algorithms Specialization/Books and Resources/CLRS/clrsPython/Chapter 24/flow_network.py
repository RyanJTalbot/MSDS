#!/usr/bin/env python3
# flow_network.py

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

from adjacency_list_graph import AdjacencyListGraph, Edge


class FlowEdge(Edge):

	def __init__(self, u, v, c, original_edge):
		"""Initialize edge to vertex v with nonnegative capacity c."""
		Edge.__init__(self, v)
		self.u = u  # this edge leaves vertex u
		self.c = c  # capacity of this edge
		self.f = 0  # flow on this edge, initially 0
		self.original_edge = original_edge 	# the corresponding edge of the original flow network
		self.reverse_edge = None

	def get_u(self):
		"""Return the vertex that this edge leaves."""
		return self.u

	def get_capacity(self):
		"""Return the capacity of this edge."""
		return self.c

	def get_flow(self):
		"""Return the flow on this edge."""
		return self.f

	def get_original_edge(self):
		"""Return the corresponding edge of the original flow network."""
		return self.original_edge

	def set_reverse_edge(self, reverse_edge):
		"""Set the reverse edge that goes from v to u."""
		self.reverse_edge = reverse_edge

	def __str__(self):
		"""Return the string representation of this edge with its flow and capacity."""
		return Edge.__str__(self) + " (" + str(self.f) + "/" + str(self.c) + ")" 


class FlowNetwork(AdjacencyListGraph):
	"""FlowNetwork is a subclass of AdjacencyListGraph."""

	def __init__(self, card_V):
		"""Initialize a flow network as a directed, unweighted graph.

		Arguments:
		card_V -- number of vertices in the flow network
		"""
		AdjacencyListGraph.__init__(self, card_V)

	def insert_edge(self, u, v, c, original_edge=None):
		"""Insert a FlowEdge into a FlowNetwork."""
		# Cannot insert multiple edges between two vertices.
		for edge in self.get_adj_list(u):
			if edge.get_v() == v:
				raise RuntimeError("An edge already exists.")

		# Append a new FlowEdge to an adjacency list and return a reference to it.
		new_edge = FlowEdge(u, v, c, original_edge)
		self.adj_lists[u].append(new_edge)
		return new_edge 

	def insert_reverse_edge(self, c, edge):
		"""Insert the reverse edge of a given FlowEdge."""
		reverse_edge = self.insert_edge(edge.get_v(), edge.get_u(), c, edge.original_edge)
		# Set the two edges as reverses of each other.
		edge.set_reverse_edge(reverse_edge)
		reverse_edge.set_reverse_edge(edge)

	def create_residual_network(self):
		"""From this flow network, create the residual network, which is the same as the original
		flow network, except with reverse edges of capacity f. Implementation differs from book to save
		edge deletion and insertion. Edges of capacity 0 are not considered in the search function.
		"""
		residual_network = FlowNetwork(self.card_V)
		for u in range(self.card_V):
			# Insert every edge with capacity c - f and its reverse edge with capacity 0.
			for edge in self.get_adj_list(u):
				v = edge.get_v()
				c = edge.get_capacity()
				f = edge.get_flow()
				edge.original_edge = edge 	# set original edge's original edge to itself

				# In the residual network, existing edges in graph have capacity c(u, v) - f(u, v)
				residual_edge = residual_network.insert_edge(u, v, c - f, edge)
				# Reverse edges have capacity f.
				residual_network.insert_reverse_edge(f, residual_edge)

		return residual_network

	def update_residual_edge(self, edge):
		"""After changing flow of edge, update the residual edge. 

		Argument:
		edge -- an edge of the residual network, containing a reference to the edge of original flow network
		"""
		c = edge.original_edge.get_capacity()
		f = edge.original_edge.get_flow()
		# Update the edge in the same direction as the original flow network.
		if edge.original_edge.get_u() == edge.get_u(): 
			edge.c = c - f
			edge.reverse_edge.c = f
		# Otherwise, the edge is in the reverse direction as the original, so
		# set capacity to f and reverse edge to c - f.
		else:
			edge.c = f
			edge.reverse_edge.c = c - f

	def copy(self):
		"""Return copy of this flow network."""
		copy = FlowNetwork(self.card_V)
		for u in range(self.card_V):
			for edge in self.get_adj_list(u):					
				copy.insert_edge(u, edge.get_v(), edge.get_capacity(), edge.get_original_edge())
		return copy
	
	def __str__(self):
		"""Return a string of the edges in this flow network."""
		result = ""
		for u in range(self.card_V):
			result += str(u) + ": "
			for edge in self.get_adj_list(u):
				result += str(edge) + " "
			result += "\n"
		return result
