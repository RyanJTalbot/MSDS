#!/usr/bin/env python3
# hash_functions.py

# Introduction to Algorithms, Fourth edition
# Tom Cormen

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

from math import floor, ceil
from miller_rabin import miller_rabin
from random import randint
import hashlib  # for cryptographic hashing


def division_hash(k, m):
    """Hash function using the division method: h(k) = k mod m.

    Arguments:
    k -- key to hash, must be an int
    m -- size of hash table
    """

    return k % m


def multiplication_hash(k, m, A=0.6180339886341244):
    """Hash function using the division method: h(k) = floor(table * (kA - floor(kA))).

    Arguments:
    k -- key to hash, must be an int
    m -- size of hash table
    A -- a constant in the range 0 < A < 1.  May be omitted."""

    return floor(m * (k * A - floor(k * A)))


def multiply_shift_hash(k, l, w=32, a=6180339886341244):
    """Hash function using the multiply-shift method: h_a(k) = (ka mod 2**w) >> (w-l).

    Arguments:
    k -- key to hash, must be an int
    l -- base-2 logarithm of hash table size, must be an integer
    w -- number of bits in a machine word.  If omitted, 32 is used.
    a -- a constant in the range 0 < a < 2**w.  May be omitted.
            For a 2/m-universal family, choose a as a random odd integer.
    """

    return ((k * a) & ((1 << w)-1)) >> (w - l)


# This function is for use only within this module.
def _choose_a(w=32):
    """Returns a random odd integer a in the range 0 < a < 2**w.

    Argument:
    w -- number of bits.  If omitted, 32 is used."""

    return randint(1, (1 << w) - 1) | 1


def find_large_prime(w, s=40):
    """Return a large prime number with w bits.

    Arguments:
    w -- number of bits in the prime number
    s -- number of trials of Miller-Rabin primality test.  If omitted, 40 is used.
    """

    lower_bound = 1 << (w-1)
    upper_bound = (1 << w) - 1
    while True:
        n = randint(lower_bound, upper_bound) | 1  # must be odd
        # miller_rabin returns False if n is composite, True if almost certainly prime.
        if miller_rabin(n, s):
            return n


def universal_hash(k, p, a, b, m):
    """Universal hash function.

    Arguments:
    k -- key to hash, must be an int
    p -- a prime number larger than every possible k
    a -- an integer constant in the range 0 < a < p
    b -- an integer constant in the range 0 <= b < p
    m -- size of hash table
    """

    return ((a * k + b) % p) % m


def cryptographic_hash(k, m, salt=''):
    """Cryptographic hash function using SHA-256.

    Arguments:
    k -- key to hash, can be any type convertible to string
    m -- size of hash table
    salt -- optional salt string to prepend to k
    """

    return int(hashlib.sha256((salt + str(k)).encode()).hexdigest(), base=16) % m


# This function is for use only within this module.
def _swap_halves(x, w):
    """Swap the two w/2-bit halves of x and return the result.

    Arguments:
    x -- number whose halves are to be swapped
    w -- total number of bits in x
    """

    return (x >> (w//2)) + (x << (w//2))


# This function is for use only within this module.
def _wee_f(k, a, w):
    """Function f used in the wee hash function.

    Arguments:
    k -- number to mangle
    a -- multiplier
    w -- word size
    """

    return _swap_halves((2*k*k + a*k) % (1 << w), w)


def wee(k, a, b, w, r, m):
    """The Wee hash function.

    Arguments:
    k -- key to hash, must be an integer
    a -- a randomly chosen odd nonnegative integer
    b -- a randomly chosen nonnegative integer
    w -- word size
    r -- number of rounds to compute the hash function
    m -- size of hash table
    """

    t = len(bin(k)) - 2  # number of bits in k
    u = ceil(t / w)  # number of words in k

    # Chop k into u w-bit words.
    chopped = []
    mask = (1 << w) - 1
    for i in range(u):
        chopped.append(k & mask)
        k = k >> w

    q = b
    for i in range(u):
        iter_f = chopped[i] + q
        for j in range(r):
            iter_f = _wee_f(iter_f, a + 2*t, w)
        q = iter_f

    return q % m


def hashpjw(s):
    """Hash s using the hashpjw hashing function.

    Argument:
    s -- a value to hash.  Converted to a string if necessary."""

    s = str(s)
    h = 0
    for char in s:
        h = (h << 4) + ord(char)
        high = h & 0xF0000000
        if high != 0:
            h ^= high >> 24
        h &= ~high
    return h


# Testing
if __name__ == "__main__":
    w = 100
    for i in range(5):
        p = find_large_prime(w)
        print(p)
        print(cryptographic_hash(p, 100))
        print(cryptographic_hash(p, 100, 'bozo'))
        a = _choose_a(32)
        print(wee(p, a, a//2, 32, 5, 150))
