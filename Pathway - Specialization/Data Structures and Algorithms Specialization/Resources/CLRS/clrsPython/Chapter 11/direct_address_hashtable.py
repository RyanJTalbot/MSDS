#!/usr/bin/env python3
# direct_address_hashtable.py

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

class DirectAddressHashTable:

	def __init__(self, m, get_key_func=None):
		"""Initialize hashtable with a direct address table of size m.

		Arguments:
		m -- size of hashtable
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.  

		Assumption:
		The keys must be unique and in the range 0 to m-1.
		"""
		self.m = m 
		self.table = [None] * m
		# If not provided a get_key function, return the object as the key.
		if get_key_func is None:
			self.get_key = lambda x: x
		else:
			self.get_key = get_key_func

	def search(self, k):
		"""Return the object at slot k, which may be None."""
		return self.table[k]

	def insert(self, x):
		"""Insert an object with a key into the table."""
		self.table[self.get_key(x)] = x

	def delete(self, x):
		"""Delete an object with key a in the table by setting slot to None."""
		self.table[self.get_key(x)] = None

	def __str__(self):
		"""Return a string representation of the table."""
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

	# Hashtable of integers. 
	hashtable1 = DirectAddressHashTable(10)
	for i in range(10):
		hashtable1.insert(i)
	print(hashtable1)
	hashtable1.delete(5)         # delete
	print(hashtable1)
	print(hashtable1.search(9))
	print(hashtable1.search(5))  # already deleted
	try:
		hashtable1.insert(11)    # out of range
	except IndexError as e:
		print(e)

	# Hashtable of objects. 
	hashtable2 = DirectAddressHashTable(20, KeyObject.get_key)
	hashtable2.insert(KeyObject("Alice", 3))
	hashtable2.insert(KeyObject("Bob", 6))
	hashtable2.insert(KeyObject("Cole", 10))
	david = KeyObject("David", 5)
	hashtable2.insert(david)	
	print(hashtable2)
	print(hashtable2.search(10))
	hashtable2.delete(david)  # delete
	print(hashtable2)
	hashtable2.delete(hashtable2.search(6))  # search then delete
	print(hashtable2)
