#!/usr/bin/env python3
# dll.py

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

class LinkedListNode:

	def __init__(self, data):
		"""Initialize a node of a doubly linked list with the given data."""
		self.prev = None
		self.next = None
		self.data = data

	def get_data(self):
		"""Return data."""
		return self.data

	def __str__(self):
		"""Return data as a string."""
		return str(self.data)


class LinkedList:

	def __init__(self, get_key_func=None):
		"""Initialize an empty doubly linked list with only a head pointer.

		Argument:
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.
		"""
		self.head = None
		if get_key_func is None:
			self.get_key = lambda x: x   # return self
		else:
			self.get_key = get_key_func  # return key defined by user

	def search(self, k):
		"""Search a doubly linked list for a node with key k.

		Returns:
		x -- a node with key k or None if not found
		"""
		x = self.head
		# get_key_func used in searching.
		while x is not None and self.get_key(x.data) != k:
			x = x.next
		return x

	def insert(self, data, y):
		"""Insert a node with data after node y.  Return the new node."""
		x = LinkedListNode(data)   # construct a node x
		x.next = y.next            # x's successor is y's successor
		x.prev = y                 # x's predecessor is y
		if y.next is not None:
			y.next.prev = x        # x comes before y's successor
		y.next = x                 # x is now y's successor
		return x

	def prepend(self, data):
		"""Insert a node with data as the head of a doubly linked list.  Return the new node."""
		x = LinkedListNode(data)   # construct a node x
		x.next = self.head         # set its next to the head
		if self.head is not None:  # if a head already exists, change its prev
			self.head.prev = x
		self.head = x              # x is the new head
		x.prev = None
		return x

	def delete(self, x):
		"""Remove a node x from a doubly linked list.

		Assumption:
		x is a node in the linked list.
		"""
		if x.prev is not None:    # if x is not the head
			x.prev.next = x.next  # connect its previous to its next
		else:
			self.head = x.next    # otherwise, set new head
		if x.next is not None:    # if x is not the tail
			x.next.prev = x.prev  # connect its next to its previous

	def delete_all(self):
		"""Delete all nodes in a doubly linked list."""
		self.head = None

	def iterator(self):
		"""Iterator from the head of a doubly linked list."""
		x = self.head
		while x is not None:
			yield x.get_data()
			x = x.next

	def copy(self):
		"""Return a copy of this doubly linked list."""
		c = LinkedList(self.get_key)  # c is the copy
		x = self.head
		if x is not None:  # start by making the head node in the copy
			last = c.prepend(x.data)  # last is the last node in the copied list
			x = x.next
		while x is not None:
			last = c.insert(x.data, last)   # append a node with x's data to c
			x = x.next
		return c

	def __str__(self):
		"""Return this doubly linked list formatted as a list."""
		x = self.head
		string = "["
		while x.next is not None:
			string += (str(x) + ", ")
			x = x.next
		string += (str(x) + "]")
		return string 


# Testing
if __name__ == "__main__":

	from key_object import KeyObject

	# Insert.
	linked_list1 = LinkedList()
	for i in range(10):
		linked_list1.prepend(i)
	print(linked_list1)

	# Search.
	print(linked_list1.search(5))

	# Copy.
	linked_list2 = linked_list1.copy()
	linked_list2.prepend(99)
	print(linked_list1)
	print(linked_list2)

	# Delete.
	linked_list2 = LinkedList()
	linked_list2.prepend(5)
	linked_list2.prepend(6)
	linked_list2.prepend(7)
	print(linked_list2)
	x = linked_list2.search(6)  # should be 6
	print(x)
	linked_list2.delete(x)
	print(linked_list2.search(6))  # unsuccessful search
	print(linked_list2)

	# Object.
	linked_list3 = LinkedList(KeyObject.get_key)
	list1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	for i in range(len(list1)):
		linked_list3.prepend(KeyObject(list1[i], i))
	print(linked_list3)
	node5 = linked_list3.search(5)  # CO has key 5
	print(node5)
	linked_list3.insert(KeyObject("VT", 17), node5)  # insert VT after CO
	linked_list3.delete(node5)                       # delete CO
	print(linked_list3)
