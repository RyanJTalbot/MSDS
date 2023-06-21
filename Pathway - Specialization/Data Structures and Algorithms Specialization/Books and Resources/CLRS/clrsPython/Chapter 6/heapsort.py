#!/usr/bin/env python3
# heapsort.py

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

from max_heap import MaxHeap

def heapsort(A):
	"""Sort a list or numpy array in place using heaps."""
	heap = MaxHeap(A)
	heap.build_max_heap()  # root is the maximum

	# Keep extracting the maximum to the just after the heap within A and then calling max_heapify.
	for i in range(len(A) - 1, 0, -1):  # len(A) - 1 down to 1
		# Swap the maximum, A[0], with A[i]
		heap.swap(0, i)
		heap.set_heap_size(heap.get_heap_size() - 1)
		# Restore the max-heap property.
		heap.max_heapify(0)


# Testing
if __name__ == "__main__":

	import numpy as np

	# Example from book.
	list1 = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
	list1test = list(list1)
	heapsort(list1)
	print(list1)
	print(list1 == sorted(list1test))

	# Repeating terms. 
	list2 = [11, 1, 51, 1, 5, 3]
	list2test = list(list2)
	heapsort(list2)
	print(list2)
	print(list2 == sorted(list2test))

	# Empty list should return empty list. 
	list3 = []
	heapsort(list3)
	print(list3)
	print(list3 == [])

	# Negative number. 
	list4 = [1, 1, -5, 6]
	list4test = list(list4)
	heapsort(list4)
	print(list4)
	print(list4 == sorted(list4test))

	# Float and int, testing numpy array. 
	array1 = np.array([11, -4, 20, 15, 13.5, -20])
	array1test = np.copy(array1)
	heapsort(array1)
	print(array1)
	print(np.array_equal(array1, np.sort(array1test)))

	# Already sorted array. 
	array2 = np.array(range(50))
	array2test = np.copy(array2)
	heapsort(array2)
	print(array2)
	print(np.array_equal(array2, np.sort(array2test)))

	# Array in reversed sorted order. 
	array3 = np.arange(50, 0, -5)
	array3test = np.copy(array3)
	print("Before sorting: ", end = '')
	print(array3)
	heapsort(array3)
	print("After sorting: ", end = '')
	print(array3)
	print(np.array_equal(array3, np.sort(array3test)))

	# Large array. 
	array4 = np.random.randint(-5000, 5000, size=1000)
	array4test = np.copy(array4)
	print("Before sorting: ", end = '')
	print(array4)
	heapsort(array4)
	print("After sorting: ", end = '')
	print(array4)
	print(np.array_equal(array4, np.sort(array4test)))
