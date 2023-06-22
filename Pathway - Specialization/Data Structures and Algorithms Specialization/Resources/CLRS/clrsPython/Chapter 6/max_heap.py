#!/usr/bin/env python3
# max_heap.py

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

from heap import Heap


class MaxHeap(Heap):

	def __init__(self, array, get_key_func=None, dict=None):
		"""Initialize a max-heap with array and heap size.

		Arguments:
		array -- array of heap elements.
		get_key_func -- an optional function that returns the key for the
		objects stored. If given, may be a static function in the object class. If
		omitted, then the identity function is used.
		dict -- an optional dictionary mapping objects in the max-heap to indices.
		"""
		Heap.__init__(self, lambda x, y: x > y, array, get_key_func, dict)

	def max_heapify(self, i):
		"""Maintain the max-heap property.

		Argument:
		i -- index of the element in the heap.
		"""
		self.heapify(i)

	def build_max_heap(self):
		"""Convert a list or numpy array into a max heap."""
		self.build_heap()


# Testing
if __name__ == "__main__":

	import numpy as np
	from key_object import KeyObject

	# Textbook example for max_heapify.
	list1 = [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]
	heap1 = MaxHeap(list1)
	heap1.max_heapify(1)
	print(str(heap1))
	print(heap1.array == [16, 14, 10, 8, 7, 9, 3, 2, 4, 1])
	print(heap1.is_heap())

	# Textbook example for build_max_heap.
	list2 = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
	heap2 = MaxHeap(list2)
	heap2.build_max_heap()
	print(str(heap2))
	print(heap2.is_heap())

	array1 = np.random.randint(-100, 100, size=50)
	heap3 = MaxHeap(array1)
	heap3.build_max_heap()
	print(str(heap3))
	print(heap3.is_heap())

	# Objects in the max-heap.
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "HI", "NH", "NY"]
	list4 = []
	for i in range(len(states)):
		list4.append(KeyObject(states[i], i))  # keys are alphabetical order
	list4 = np.random.permutation(list4)
	mapping = {}
	heap4 = MaxHeap(list4, get_key_func=KeyObject.get_key, dict=mapping)
	heap4.build_max_heap()
	print(str(heap4))
	print(heap4.is_heap())
	# Check that the mapping is correct.
	mapping_OK = True
	for i in range(heap4.get_heap_size()):
		obj = heap4.get_array()[i]
		if mapping[obj] != i:
			print("Mapping error: " + str(obj) + " maps to " + str(mapping[obj]) + ", should map to " + str(i))
			mapping_OK = False
	print(mapping_OK)

	# Check for a non-empty dictionary.
	try:
		heap5 = MaxHeap(list4, get_key_func=KeyObject.get_key, dict=mapping)
	except RuntimeError as e:
		print(e)
