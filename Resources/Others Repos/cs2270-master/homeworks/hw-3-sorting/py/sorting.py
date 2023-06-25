#
#  sorting.py
#
#  Your Name:
#  Your TA:
#  Your Collaborators:
#
#  This defines the names of various sorting functions and related
#  helper functions. You are required to implement all of these.
#  When the user calls the sorting functions, it is expected that the
#  input data is sorted in _nondecreasing_ order.  E.g.
#
#  input:  9, 5, 4, 1, 10, 5
#  output: 1, 4, 5, 5, 9, 10 



#  This is the main quicksort function. It should use the
#  quicksort_partition function. It is also recursive, so you will
#  call quicksort from inside the quicksort function.
#  
#  data: The input is a list of integers. Python objects are passed by
#  reference so whatever you do to this will be visible outside the
#  function as well.
# 
#  low_idx and high_idx: these are the current indices for the
#  quicksort algorithm. Both of these indices are inclusive: they
#  refer to an addressable element of the data vector.
#
#  This doesn't return anything: the result is stored in 'data'.
def quicksort(data, low_idx, high_idx):
    pass

#  This is the partition function for quicksort. Input parameters have
#  same semantics as for quicksort. An additional parameter is given
#  for the pivot location. 
# 
#  The modified pivot location is returned. 
def quicksort_partition(data, low_idx, high_idx, pivot_index):
    pass

#  The bubblesort is probably the easiest sorting algorithm to
#  conceive of. It is unfortunately not all that fast. Here's your
#  chance to write really inefficient code! There are no related
#  helper functions.
#
#  This doesn't return anything: the result is stored in 'data'.
def bubblesort(data):
    pass

#  The mergesort is another classic O(n log n) sorting algorithm. This
#  uses the helper function 'merge'.
#
#  This doesn't return anything: the result is stored in 'data'.
def mergesort(data):
    pass

#  merge is the helper function for mergesort. It returns a vector
#  containing the merged contents of the two input vectors.
def merge(left, right):
    pass

#  You may implement any additional sorting function you wish, and
#  call it 'mystery_sort'.
#  
#  See http://en.wikipedia.org/wiki/Sorting_algorithm for a list.
# 
#  Only rules are: (1) it has to have the following signature, and the
#  calling code will expect 'data' to be in non-decreasing order when
#  it returns, and (2) you have to write something new---no relying on
#  the other functions you've implemented.
#
#  This doesn't return anything: the result is stored in 'data'.
def mystery_sort(data):
    pass

