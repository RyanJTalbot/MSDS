#!/usr/bin/env python3
# open_address_hash table.py

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

class Deleted:
	"""Unique object to signify when hash table element has been deleted."""
	def __init__(self):
		self.key = None

	def __str__(self):
		return "deleted"


def linear_probing_hash_function(h):
	"""Return a function that performs linear probing.
	Parameter:
	h -- a primary hash function

	Returns:
	A function with parameters:
		h -- primary hash function
		k -- key to be hashed
		i -- iteration number
		m -- size of hash table
	"""
	return lambda k, i, m: (h(k) + i) % m


def inverse_linear_probing_hash_function(h):
	"""Return a function that performs the inverse function of linear probing.

	Parameter:
	h -- a primary hash function

	Returns:
	A function with parameters:
		h -- a primary hash function
		x -- object to be hashed
		q -- a slot number
		m -- size of hash table
	"""
	return lambda k, q, m: (q - h(k)) % m


def double_hashing_hash_function(h1, h2):
	"""Return a function that probes slot positions offset by a second hash function.
	Parameters:
	h1 -- a primary hash function
	h2 -- a secondary hash function

	Returns:
	A function with parameters:
		h1 -- a primary hash function
		h2 -- a secondary hash function
		k -- key to be hashed
		i -- iteration number
		m -- size of hash table
	"""
	return lambda k, i, m: (h1(k) + i * h2(k)) % m


class OpenAddressHashTable:

	def __init__(self, m, h1, h2=None, get_key_func=None):
		"""Initialize hash table with a direct address table of size m.

		Arguments:
		m -- size of hash table
		h1 -- function that determines a slot number given a key and
		an iteration number in the probe sequence
		h2 -- auxiliary hash function for double hashing; if None, then using
		linear probing
		get_key_func -- an optional function that returns the key for the
		objects stored. May be a static function in the object class. If 
		omitted, then identity function is used.
		linear-probing -- True if the hash function uses linear probing, False otherwise.
		Determines whether to use the Deleted marker.
		"""
		self.m = m
		self.table = [None] * m

		# If not provided a get_key function, return the object as the k.
		if get_key_func is None:
			self.get_key = lambda x: x
		else:
			self.get_key = get_key_func

		if h2 is None:  # using linear probing
			self.hash_func = linear_probing_hash_function(h1)
			self.deleted = None
			self.open_slot = lambda q: self.table[q] is None
			self.delete = self.linear_probing_hash_delete
			self.g = inverse_linear_probing_hash_function(h1)
		else:
			self.hash_func = double_hashing_hash_function(h1, h2)
			self.deleted = Deleted()
			self.open_slot = lambda q: self.table[q] is None or self.table[q] == self.deleted
			self.delete = self.double_hashing_hash_delete

	def insert(self, x):
		"""Insert x into hash table and return its slot number."""
		i = 0
		# Continue probing until finding an empty slot or have searched every element.
		for i in range(self.m):
			q = self.hash_func(self.get_key(x), i, self.m)
			if self.open_slot(q):  # insert into this empty slot
				self.table[q] = x
				return q  # return slot number

		# If all m probes found occupies slots, the hash table is full.
		raise RuntimeError("Cannot insert: hash table is full")

	def search(self, k):
		"""Search for and object with key k.

		Returns:
		Index of object. 
		"""
		# Empty hash table.
		if self.m == 0:
			return None
		i = 0 
		# Continue probing until finding an element with key k, finding an empty slot,
		# or have searched all m slots.
		while True:
			q = self.hash_func(k, i, self.m)
			if self.table[q] is None:  # empty slot
				return None  # not found
			elif self.get_key(self.table[q]) == k:
				return q  # found the object in slot q
			else:
				i += 1
				if i == self.m:  # searched entire table?
					return None  # not found

	def double_hashing_hash_delete(self, k):
		"""Delete an object from the hash table by replacing it with self.deleted."""
		q = self.search(k)  # index of the slot where the object is located
		if q is None:  # if not found
			raise RuntimeError("Cannot delete: " + str(k) + " is not in hash table")
		self.table[q] = self.deleted 	# slot now contains self.deleted

	def linear_probing_hash_delete(self, k):
		"""Delete an object from the hash table, knowing that linear probing is used."""
		q = self.search(k)  # index of the slot where the object is located
		if q is None:  # if not found
			raise RuntimeError("Cannot delete: " + str(k) + " is not in hash table")

		while True:
			self.table[q] = None  # make slot q empty
			q_prime = q  # starting point for search
			while True:
				q_prime = (q_prime + 1) % self.m  # next slot number with linear probing
				k_prime = self.table[q_prime]  # next object to try to move
				if k_prime is None:
					return  # return when an empty slot is found
				k_prime_key = self.get_key(k_prime)  # key of object k_prime
				if self.g(k_prime_key, q, self.m) < self.g(k_prime_key, q_prime, self.m):  # was empty slot q probed before q_prime?
					break
			self.table[q] = k_prime  # move k_prime into slot q
			q = q_prime  # free up slot q_prime

	def __str__(self):
		"""Return table when str called."""
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

	# Hashtable of integers with linear probing.
	hashtable1 = OpenAddressHashTable(10, hashpjw)
	for i in [2, 3, 5, 7, 11, 13, 19, 23, 25, 29]:
		print("h(" + str(i) + ") = " + str(hashtable1.hash_func(hashtable1.get_key(i), 0, hashtable1.m)))
		hashtable1.insert(i)
		print(hashtable1)
	x = hashtable1.search(23)
	print(x)
	hashtable1.delete(5)		# delete
	print(hashtable1)
	print(hashtable1.search(25))
	print(hashtable1.search(5))  # unsuccessful search
	try:
		hashtable1.delete(5)     # already deleted
	except RuntimeError as e:
		print(e)
	i = 31
	print("h(" + str(i) + ") = " + str(hashtable1.hash_func(hashtable1.get_key(i), 0, hashtable1.m)))
	hashtable1.insert(i)		# should go into one empty space
	print(hashtable1)
	try:
		hashtable1.insert(12)   # hash table is already full
	except RuntimeError as e:
		print(e)
	print()

	# Same, but using deleted marker to identify deleted slots.
	hashtable2 = OpenAddressHashTable(10, hashpjw, lambda x: 1)
	for i in [2, 3, 5, 7, 11, 13, 19, 23, 25, 29]:
		print("h(" + str(i) + ") = " + str(hashtable2.hash_func(i, 0, hashtable2.m)))
		hashtable2.insert(i)
		print(hashtable2)
	x = hashtable2.search(23)
	print(x)
	hashtable2.delete(5)		# delete
	print(hashtable2)
	print(hashtable2.search(25))
	print(hashtable2.search(5))  # unsuccessful search
	try:
		hashtable2.delete(5)     # already deleted
	except RuntimeError as e:
		print(e)
	i = 31
	print("h(" + str(i) + ") = " + str(hashtable2.hash_func(i, 0, hashtable2.m)))
	hashtable2.insert(i)		# should go into one empty space
	print(hashtable2)
	try:
		hashtable2.insert(12)   # hash table is already full
	except RuntimeError as e:
		print(e)
	print()

	# Hash table of objects with linear probing.
	hashtable3 = OpenAddressHashTable(10, hashpjw, None, KeyObject.get_key)
	objs = [KeyObject("Asparagus", 2), KeyObject("Banana", 3), KeyObject("Carrot", 5),
			KeyObject("Dill", 7), KeyObject("Escarole", 11), KeyObject("Fava bean", 13),
			KeyObject("Garlic", 19), KeyObject("Haricot", 23), KeyObject("Iceberg lettuce", 25),
			KeyObject("Jicama", 29)]
	for i in objs:
		print("h(" + str(i) + ") = " + str(hashtable3.hash_func(hashtable3.get_key(i), 0, hashtable3.m)))
		hashtable3.insert(i)
		print(hashtable3)
	x = hashtable3.search(23)
	print(x)
	hashtable3.delete(5)		# delete
	print(hashtable3)
	print(hashtable3.search(25))
	print(hashtable3.search(5))  # unsuccessful search
	try:
		hashtable3.delete(5)     # already deleted
	except RuntimeError as e:
		print(e)
	i = KeyObject("Kale", 31)
	print("h(" + str(i) + ") = " + str(hashtable3.hash_func(hashtable3.get_key(i), 0, hashtable3.m)))
	hashtable3.insert(i)		# should go into one empty space
	print(hashtable3)
	try:
		hashtable3.insert(KeyObject("Lemon", 12))   # hash table is already full
	except RuntimeError as e:
		print(e)
	print()

	# Double hashing
	def aux_hash_func(k):
		return k % 701
	hashtable4 = OpenAddressHashTable(15, hashpjw, aux_hash_func, KeyObject.get_key)
	for i in range(14):
		obj = KeyObject(str(i), 37 * i)
		print("h(" + str(obj) + ") = " + str(hashtable4.hash_func(hashtable4.get_key(obj), 0, hashtable4.m)))
		hashtable4.insert(obj)
		print(hashtable4)
	obj1 = KeyObject("Last element", 14)
	print("h(" + str(obj1) + ") = " + str(hashtable4.hash_func(hashtable4.get_key(obj1), 0, hashtable4.m)))
	hashtable4.insert(obj1)
	print(hashtable4)
	i = 5
	hashtable4.delete(37 * i)
	print(hashtable4)
	try:
		hashtable4.delete(37 * i)  # already deleted
	except RuntimeError as e:
		print(e)
	print()

	# No get_key function.
	hashtable5 = OpenAddressHashTable(10, hashpjw, None, None)
	hashtable5.insert(KeyObject("hello", "world"))
	hashtable5.insert(KeyObject("stranger", "things"))
	porthos = KeyObject("second", "musketeer")
	hashtable5.insert(porthos)
	print(hashtable5)
	print(hashtable5.search(porthos))
	hashtable5.delete(porthos)
	print(hashtable5)
