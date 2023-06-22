#!/usr/bin/env python3
# min_heap_priority_queue.py

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

"""Base class for MaxHeapPriorityQueue and MinHeapPriorityQueue."""

from heap import Heap


class HeapPriorityQueue:

    def __init__(self, compare, temp_insert_value, get_key_func, set_key_func=None):
        """Initialize minimum priority queue implemented with a heap.

        Arguments:
        compare -- comparison function: greater-than for a max-heap priority queue,
        less-than for a min-heap priority queue
        temp_insert_value -- temporary value given to objects upon insertion, then
        changed to the actual value of the object
        get_key_func -- required function that returns the key for the
        objects stored. May be a static function in the object class.
        set_key_func -- optional function that sets the key for the objects
        stored. May be a static function in the object class.
        """

        # Dictionary to map array objects to array indices.
        # Mapping might not take worst-case time O(1).
        self.dict = {}

        # self.get_key function used to get key of object.
        self.get_key = get_key_func

        # self.set_key function used to set key of object.
        self.set_key = set_key_func

        # Initialize to empty heap.
        self.heap = Heap(compare, [], self.get_key, self.dict)
        self.compare = compare
        self.temp_insert_value = temp_insert_value

    def get_heap(self):
        """Return heap, used in testing."""
        return self.heap

    def get_size(self):
        """Return the number of objects in the priority queue."""
        return self.heap.get_heap_size()

    def top_of_heap(self):
        """Return the object at the top of the heap."""
        if self.heap.get_heap_size() <= 0:  # error if heap is empty
            raise RuntimeError("Heap underflow.")
        return self.heap.get_array()[0]

    def extract_top(self):
        """Return and delete the top element in a heap."""
        top = self.top_of_heap()

        # Move the last object in heap to the root position.
        last_obj = self.heap.get_array()[self.heap.get_heap_size()-1]
        self.heap.get_array()[0] = last_obj
        self.dict[last_obj] = 0

        # Remove the old top object.
        del self.dict[top]
        self.heap.set_heap_size(self.heap.get_heap_size() - 1)

        # Restore the heap property.
        self.heap.heapify(0)

        # Return the top item, which was extracted.
        return top

    def update_key(self, x, k):
        """Update the key of object x to value k.
        Assumption: The caller has already verified that the new value is OK.

        Arguments:
        x -- object whose key has been changed
        k -- new key of x
        """
        if self.set_key is not None:
            self.set_key(x, k)

        # Get the index from the dictionary.
        i = self.dict[x]

        # Compare the value with parents up the heap to place in the correct position.
        while i > 0 and \
                self.compare(self.get_key(self.heap.get_array()[i]),
                             self.get_key(self.heap.get_array()[self.heap.parent(i)])):
            # Exchange positions and continue if the element should head toward the root.
            self.heap.swap(i, self.heap.parent(i))
            i = self.heap.parent(i)

    def insert(self, x):
        """Insert x into the heap.  Grows the heap as necessary.

        Arguments:
        x -- object to insert
        """

        # Increment the heap size.
        self.heap.set_heap_size(self.heap.get_heap_size() + 1)

        k = self.get_key(x)

        if self.set_key is not None:
            self.set_key(x, self.temp_insert_value)

        # Insert x into the array and the dictionary.
        self.heap.get_array().insert(self.heap.get_heap_size() - 1, x)
        self.dict[x] = self.heap.get_heap_size() - 1

        # Maintain the heap property.
        self.update_key(x, k)

    def is_heap(self):
        """Verify that the array or list represents a heap."""
        return self.heap.is_heap()

    def __str__(self):
        """Return the heap as an array."""
        return str(self.heap)
