#!/usr/bin/env python3
# lifo_stack.py

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

import numpy as np


class Stack:

	def __init__(self, n=4):
		"""Initialize a stack with an array of length n."""
		self.stack = [None] * n
		self.size = n
		self.top = -1 	# index of the top element

	def is_empty(self):
		"""Return a boolean indicating whether the stack is empty."""
		return self.top == -1

	def push(self, x):
		"""Add an element to the top of the stack."""
		if self.top == self.size - 1:
			raise RuntimeError("Stack overflow")
		else:
			self.top += 1
			self.stack[self.top] = x

	def pop(self):
		"""Remove the top element from the stack and return it."""
		if self.is_empty():
			raise RuntimeError("Stack underflow.")
		else:
			self.top -= 1
			return self.stack[self.top + 1]

	def __str__(self):
		"""Print the stack up to top element."""
		return str(self.stack[:self.top + 1])


# Testing
if __name__ == "__main__":

	stack1 = Stack(5)
	print(stack1)
	stack1.push(1)
	print(stack1)  # one element: 1
	stack1.push(2)
	stack1.push(100)
	print(stack1)  # three elements: 1, 2, 100
	print(stack1.pop()) 	# pop 100 out
	print(stack1)
	print(stack1.pop()) 	# pop 2 out
	print(stack1.pop()) 	# pop 1 out
	print(stack1.is_empty())  # should be true
	try:
		stack1.pop() 	# error when popping empty stack
	except RuntimeError as e:
		print(e)

	# Check for overflow.
	stack2 = Stack(10)
	for i in range(11):
		try:
			stack2.push(i)
		except RuntimeError as e:
			print(e)
	print(stack2)