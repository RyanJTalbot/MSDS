/*

  sorting.cpp

  Please refer to sorting.h for documentation on each function.

  Your Name:
  Your TA:
  List O' Collaborators:


   + ------ N O T E: -- Big scary warning! ------------------------------
   |
   |    We clearly can't use unit testing to ensure that you're
   |    actually implementing the correct algorithm. I suppose we could
   |    write some complicated static analysis checker. But it is
   |    easier to just look at it with our eyeballs.
   |
   |    After the assignment is due, we will look at the most recent
   |    version of your implementation that got the highest score and
   |    make sure you're not doing something sneaky like using a
   |    standard library call to sort a vector.
   |
   |    Anyone caught doing this (even though it is kinda funny) will
   |    be given 0/15 on the assignment.
   |
   +-------------------------------------------------------------------- 

 */

#include "sorting.h"

using namespace std;


void quicksort(vector<int> &data, int low_idx, int high_idx) {
  // implement me
}

int quicksort_partition(vector<int> &data, int low_idx, int high_idx,
			int pivot_index) {
  // implement me

}

void bubblesort(vector<int> &data) {
  // implement me

}

void mergesort(vector<int> &data) {
  // implement me

}

vector<int> merge(vector<int> &left, vector<int> &right) {
  // implement me

}

void mystery_sort(vector<int> &data) {
  // implement me. choose a different sorting algorithm and go to
  // town.

}

