#!/usr/bin/env python3
# max_heap_priority_queue.py

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

from heap_priority_queue import HeapPriorityQueue


class MaxHeapPriorityQueue(HeapPriorityQueue):

	def __init__(self, get_key_func, set_key_func=None):
		"""Initialize a maximum priority queue implemented with a heap.

		Arguments:
		get_key_func -- required function that returns the key for the
		objects stored. May be a static function in the object class.
		set_key_func -- optional function that sets the key for the objects
		stored. May be a static function in the object class.
		"""
		HeapPriorityQueue.__init__(self, lambda x, y: x > y, float('-inf'), get_key_func, set_key_func)

	def maximum(self):
		"""Return the object with the maximum key in a heap."""
		return self.top_of_heap()

	def extract_max(self):
		"""Return and delete the object with the maximum value in a heap."""
		return self.extract_top()

	def increase_key(self, x, k):
		"""Increase the key of object x to value k.  Error if k is less than x's current key.
			Update the heap structure appropriately.

		Arguments: 
		x -- object whose key has been increased
		k -- new key of x
		"""

		if k < self.get_key(x):
			raise RuntimeError("Error in increase_key: new key " + str(k)
							   + " is less than current key " + str(x.get_key()))

		# Make the changes in the heap.
		self.update_key(x, k)

	def insert(self, x):
		"""Insert x into the max heap.  Grows the heap as necessary."""
		HeapPriorityQueue.insert(self, x)


# Testing
if __name__ == "__main__":

	import numpy as np
	from key_object import KeyObject

	# Must use objects.
	list1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	pq1 = MaxHeapPriorityQueue(KeyObject.get_key, KeyObject.set_key)
	for i in range(len(list1)):
		pq1.insert(KeyObject(list1[i], i))
	print(pq1)
	print(pq1.get_heap().is_heap())

	# Increase last key to 100 which should be the maximum.
	# Last element (AZ) should be first. 
	e = pq1.get_heap().get_array()[len(list1) - 1]
	pq1.increase_key(e, 100)
	print(pq1)
	print(pq1.get_heap().is_heap())

	# New maximum should be the element with the increased key.
	maximum = pq1.extract_max()
	print(maximum)
	print(maximum == e)
	print(pq1)

	# Check repeated calls to extract_max.
	extracted_keys = []
	while pq1.get_size() > 0:
		max_element = pq1.extract_max()
		extracted_keys.insert(0, KeyObject.get_key(max_element))
	print(extracted_keys)
	print(extracted_keys == sorted(extracted_keys))

	# Check maximum in empty priority queue.
	pq2 = MaxHeapPriorityQueue(KeyObject.get_key, KeyObject.set_key)
	try:
		maximum = pq2.extract_max()
		print(KeyObject.get_key(maximum))
	except RuntimeError as e:
		print(e)
