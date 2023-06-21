#!/usr/bin/env python3
# chained_hashtable.py

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


class ChainedHashTable:

	def __init__(self, m, hash_func=hash, get_key_func=None):
		"""Initialize each slot with a linkedlist. 

		Arguments:
		m -- size of hashtable
		hash_func -- hash function to use. If omitted, uses the builtin	Python function 'hash'.
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then the identity function is used.
		"""
		self.m = m 
		self.table = [None] * m
		# Initialize every slot in the table with a linked list.
		for i in range(m):
			self.table[i] = DLLSentinel(get_key_func)
		self.hash_function = hash_func
		# If not provided a get_key function, return the object as the key.
		if get_key_func is None:
			self.get_key = lambda x: x
		else:
			self.get_key = get_key_func

	def insert(self, data):
		"""Insert an object into the linked list at the appropriate table slot."""
		self.table[self.hash_function(self.get_key(data)) % self.m].prepend(data)

	def search(self, key):
		"""Return an object with a given key or None if not found."""
		return self.table[self.hash_function(key) % self.m].search(key)

	def delete(self, node):
		"""Delete an object with a given key from the linked list at the appropriate table slot."""
		self.table[self.hash_function(self.get_key(node.data)) % self.m].delete(node)

	def __str__(self):
		"""Return the string representation of this hash table, looking like a Python list."""
		string = "["
		if self.m > 0:
			for i in range(self.m - 1):
				string += str(self.table[i]) + ", "
			string += str(self.table[self.m - 1])
		string += "]"
		return string


# Testing
if __name__ == "__main__":

	from key_object import KeyObject
	from hash_functions import hashpjw

	# Hashtable of integers.
	hashtable1 = ChainedHashTable(10)
	for i in range(10):
		hashtable1.insert(i)
	print(hashtable1)
	x = hashtable1.search(5)
	hashtable1.delete(x)         # delete
	print(hashtable1)
	print(hashtable1.search(9))
	print(hashtable1.search(5))  # already deleted
	hashtable1.insert(11)        # appends to linked list
	print(hashtable1)
	print()

	# Hashtable of objects.
	hashtable2 = ChainedHashTable(20, hash_func=hashpjw, get_key_func=KeyObject.get_key)
	hashtable2.insert(KeyObject("Alice", 3))
	hashtable2.insert(KeyObject("Bob", 6))
	hashtable2.insert(KeyObject("Cindy", 10))
	hashtable2.insert(KeyObject("David", 5))
	print(hashtable2)
	x = hashtable2.search(5)
	print(x)
	hashtable2.delete(x)  # delete object with "David"
	print(hashtable2)
