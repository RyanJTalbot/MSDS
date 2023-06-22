#!/usr/bin/env python3
# fifo_queue.py

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

class Queue:

	def __init__(self, n):
		"""Initialize a queue of n elements."""
		self.array = [None] * (n+1)  # queue
		self.size = n
		self.head = 0  # index of head
		self.tail = 0  # index of the next location where a new element will be inserted

	def is_empty(self):
		"""Return a boolean indicating whether the queue is empty."""
		return self.head == self.tail

	def enqueue(self, x):
		"""Add an element to the tail of the queue."""
		# Check for queue overflow. Must always have at least 1 empty slot.
		if self.head == (self.tail + 1) % self.size:
			raise RuntimeError("Queue is full.")
		self.array[self.tail] = x
		# Wrap around index of tail if the end of the array is reached.
		self.tail = (self.tail + 1) % self.size

	def dequeue(self):
		"""Remove an element from the head of the queue."""
		if self.is_empty():  # queue underflow?
			raise RuntimeError("Queue is empty.")
		else:
			x = self.array[self.head]
			# Wrap around the index of the head if the end of the array is reached.
			self.head = (self.head + 1) % self.size
			return x

	def __str__(self):
		"""Return the string representation of the queue, from head to tail."""
		if self.is_empty():
			return str([])
		elif self.head <= (self.tail - 1) % self.size:
			return str(self.array[self.head: ((self.tail - 1) % self.size) + 1])
		else:
			return str(self.array[self.head:] + self.array[: self.tail])


# Testing
if __name__ == "__main__":

	# Textbook example.
	queue1 = Queue(11)
	# Put in 6 values.
	for i in range(100, 106):
		queue1.enqueue(i)
	print(queue1)  # should print True
	for i in range(6):
		print(queue1.dequeue())
	print(queue1.is_empty())
	queue1.enqueue(15)
	queue1.enqueue(6)
	queue1.enqueue(9)
	queue1.enqueue(8)
	queue1.enqueue(4)
	print(queue1)
	queue1.enqueue(17)
	print(queue1)
	queue1.enqueue(3)
	print(queue1)
	queue1.enqueue(5)
	print(queue1)
	print(queue1.dequeue())
	print(queue1)

	# Empty queue1 and then try to dequeue.
	while not queue1.is_empty():
		queue1.dequeue()
	try:
		queue1.dequeue()  # error when dequeueing from empty queue
	except RuntimeError as e:
		print(e)

	# Queue overflow.
	queue2 = Queue(10)
	for i in range(9):
		queue2.enqueue(i)
	print(queue2)
	try:
		queue2.enqueue(10)
	except RuntimeError as e:
		print(e)
