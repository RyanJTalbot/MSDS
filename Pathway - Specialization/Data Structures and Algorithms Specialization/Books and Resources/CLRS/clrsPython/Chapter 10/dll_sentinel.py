#!/usr/bin/env python3
# dll_sentinel.py

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

class LinkedListNode:

	def __init__(self, data):
		"""Initialize a node of a circular doubly linked list with a sentinel with the given data."""
		self.prev = None
		self.next = None
		self.data = data

	def get_data(self):
		"""Return data."""
		return self.data

	def __str__(self):
		"""Return data as a string."""
		return str(self.data)


class DLLSentinel:

	def __init__(self, get_key_func=None):
		"""Initialize the sentinel of a circular doubly linked list with a sentinel.

		Arguments:
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.
		"""
		self.sentinel = LinkedListNode(None)  # holds None as data
		self.sentinel.next = self.sentinel  # the sentinel points to itself in an empty list
		self.sentinel.prev = self.sentinel

		if get_key_func is None:
			self.get_key = lambda x: x   # return self
		else:
			self.get_key = get_key_func  # return key defined by user

	def search(self, k):
		"""Search a circular doubly linked list with a sentinel for a node with key k.

		Returns:
		x -- node with key k or None if not found
		"""
		x = self.sentinel.next
		# Go down the list until key k is found.
		# Need to test for the sentinel to avoid calling get_key(None) when x is the sentinel.
		while x is not self.sentinel and self.get_key(x.data) != k:
			x = x.next

		if x is self.sentinel:  # went through the whole list?
			return None         # yes, so no node had key
		else:
			return x            # found it!

	def insert(self, data, y):
		"""Insert a node with data after node y.  Return the new node."""
		x = LinkedListNode(data)   # construct a node x
		x.next = y.next            # x's successor is y's successor
		x.prev = y                 # x's predecessor is y
		y.next.prev = x            # x comes before y's successor
		y.next = x                 # x is now y's successor
		return x

	def prepend(self, data):
		"""Insert a node with data as the head of a circular doubly linked list with a sentinel.
		Return the new node."""
		return self.insert(data, self.sentinel)

	def append(self, data):
		"""Append a node with data to the tail of a circular doubly linked list with a sentinel.
		Return the new node."""
		return self.insert(data, self.sentinel.prev)

	def delete(self, x):
		"""Remove a node x from the a circular doubly linked list with a sentinel.

		Assumption:
		x is a node in the linked list. 
		"""
		if x is self.sentinel:
			raise RuntimeError("Cannot delete sentinel.")
		x.prev.next = x.next  # point prev to next
		x.next.prev = x.prev  # point next to prev

	def delete_all(self):
		"""Delete all nodes in a circular doubly linked list with a sentinel."""
		self.sentinel.next = self.sentinel
		self.sentinel.prev = self.sentinel

	def iterator(self):
		"""Iterator from the head of a circular doubly linked list with a sentinel."""
		x = self.sentinel.next
		while x is not self.sentinel:
			yield x.get_data()
			x = x.next

	def copy(self):
		"""Return a copy of this circular doubly linked list with a sentinel."""
		c = DLLSentinel(self.get_key)      # c is the copy
		x = self.sentinel.next
		while x != self.sentinel:
			c.append(x.data)   # append a node with x's data to c
			x = x.next
		return c

	def __str__(self):
		"""Return this circular doubly linked list with a sentinel formatted as a list."""
		x = self.sentinel.next
		string = "["
		while x != self.sentinel:
			string += (str(x) + ", ")
			x = x.next
		string += (str(x) + "]")
		return string


# Testing
if __name__ == "__main__":

	from key_object import KeyObject

	# Insert. 
	linked_list1 = DLLSentinel()
	for i in range(10):
		linked_list1.prepend(i)
	print(linked_list1)

	# Search. 
	print(linked_list1.search(5))

	# Copy.
	linked_list2 = linked_list1.copy()
	linked_list2.append(99)
	print(linked_list1)
	print(linked_list2)
	
	# Delete. 
	linked_list2 = DLLSentinel()
	linked_list2.prepend(5)
	linked_list2.prepend(6)
	linked_list2.prepend(7)
	print(linked_list2)
	x = linked_list2.search(6)  # should be 6
	print(x)
	linked_list2.delete(x)
	print(linked_list2.search(6))  # unsuccessful search
	print(linked_list2)

	# Delete sentinel error. 
	try:
		linked_list2.delete(linked_list2.sentinel)
	except RuntimeError as e:
		print(e)

	# Object.
	linked_list3 = DLLSentinel(KeyObject.get_key)
	list1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	for i in range(len(list1)):
		linked_list3.append(KeyObject(list1[i], i))
	print(linked_list3)
	node5 = linked_list3.search(5)  # CO has key 5
	print(node5)
	linked_list3.insert(KeyObject("VT", 17), node5)  # insert VT after CO
	linked_list3.delete(node5)                       # delete CO
	print(linked_list3)
