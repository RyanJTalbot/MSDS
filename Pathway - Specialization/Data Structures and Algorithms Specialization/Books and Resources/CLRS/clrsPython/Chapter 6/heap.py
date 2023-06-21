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

"""Base class for MaxHeap and MinHeap."""


class Heap:
    def __init__(self, compare, array, get_key_func=None, dict=None):
        """Initialize a heap with an array and heap size.

        Arguments:
        compare -- comparison function: greater-than for a max-heap, less-than for a min-heap
        array -- array of heap elements.
        get_key_func -- an optional function that returns the key for the
        objects stored. If given, may be a static function in the object class. If
        omitted, then the identity function is used.
        dict -- an optional dictionary mapping objects in the max-heap to indices.
        """
        self.compare = compare
        self.array = array
        # heap_size is the number of elements in the heap that are stored
        # in the array, defaults to all elements in array.
        self.heap_size = len(array)
        if get_key_func is None:
            self.get_key = lambda x: x
        else:
            self.get_key = get_key_func

        # If there is a dictionary mapping objects to indices, initialize it.
        # It should be empty to start.
        self.dict = dict
        if self.dict is not None:
            if len(self.dict) > 0:
                raise RuntimeError("Dictionary argument to constructor must be None or an empty dictionary.")
            for i in range(self.heap_size):
                dict[self.array[i]] = i

    def get_heap_size(self):
        """Return the size of this heap."""
        return self.heap_size

    def is_full(self):
        """Return True if this heap is full, False if not full."""
        return self.heap_size >= len(self.array)

    def get_array(self):
        """Return the array implementation of this heap."""
        return self.array

    def set_heap_size(self, size):
        """Set heap size to given size."""
        self.heap_size = size

    def parent(self, i):
        """Return the index of the parent node of i."""
        return (i-1) // 2

    def left(self, i):
        """Return the index of the left child of i."""
        return 2*i + 1

    def right(self, i):
        """Return the index of the right child of i. """
        return 2*i + 2

    def swap(self, i, j):
        """Swap two elements in an array."""
        if self.dict is not None:
            self.dict[self.array[i]] = j
            self.dict[self.array[j]] = i
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def heapify(self, i):
        """Maintain the heap property.

        Argument:
        i -- index of the element in the heap.
        """
        l = self.left(i)
        r = self.right(i)

        if l < self.heap_size and self.compare(self.get_key(self.array[l]), self.get_key(self.array[i])):
            swap_with = l
        else:
            swap_with = i

        if r < self.heap_size and self.compare(self.get_key(self.array[r]), self.get_key(self.array[swap_with])):
            swap_with = r

        if swap_with != i:
            self.swap(i, swap_with)
            self.heapify(swap_with)

    def build_heap(self):
        """Convert a list or numpy array into a heap."""
        # Run heapify on all roots of the tree, from ((heap_size // 2) - 1) to 0.
        self.heap_size = len(self.array)
        for i in range((len(self.array) // 2) - 1, -1, -1):
            self.heapify(i)

    def __str__(self):
        """Return the heap as an array."""
        return ", ".join(str(x) for x in self.array[:self.heap_size])

    def is_heap(self):
        """Verify that the array or list represents a heap."""
        # From root node to last internal node.
        for i in range(0, self.heap_size // 2):
            # Check the left child.
            if self.compare(self.get_key(self.array[self.left(i)]), self.get_key(self.array[i])):
                return False
            # If there is a right child, check it.
            if self.right(i) < self.heap_size and \
                    self.compare(self.get_key(self.array[self.right(i)]), self.get_key(self.array[i])):
                return False

        return True
