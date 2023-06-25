/*

  sorting_driver.cpp

*/

#include <cstring>
#include <cstdlib>
#include "sorting.h"
#include "UTFramework.h"

using namespace Thilenius;
using namespace std;

extern int RETROGRADE_MODE;

vector<int> get_random_data(int how_many, int upper_bound);

bool vector_contains(vector<int> &data, int value);

bool vectors_contain_same(vector<int>& blue, vector<int> &green);

bool is_nondecreasing(vector<int> &data);

vector<int> get_copy(vector<int> &data);

SUITE_BEGIN("Sorting")

//  IsTrue("Returned A Node", four != NULL, 
//	 "A Null node was returned by the init_node( ) function.");

TEST_BEGIN("Sanity Check")
{
  vector<int> data;
  data.push_back(5);
  data.push_back(25);
  data.push_back(35);
  data.push_back(25);
  data.push_back(55);

  vector<int> response;
  response.push_back(5);
  response.push_back(25);
  response.push_back(30);
  response.push_back(25);
  response.push_back(5);

  vector<int> good_response;
  good_response.push_back(5);
  good_response.push_back(25);
  good_response.push_back(25);
  good_response.push_back(35);
  good_response.push_back(55);

  IsTrue("Has 5", vector_contains(data, 5), 
	 "data should have 5 in it.");
  IsTrue("Doesn't have 6", !vector_contains(data, 6), 
	 "data should not have 6 in it.");
  IsTrue("Not same vals", !vectors_contain_same(data, response), 
	 "shouldn't contain same");
  IsTrue("Same vals", vectors_contain_same(data, good_response), 
	 "Should have same data");
  IsTrue("Bad Nondecrease", !is_nondecreasing(response), 
	 "Response is not sorted but we think it is");
  IsTrue("Good Nondecrease", is_nondecreasing(good_response), 
	 "Good response is sorted but we think it isn't.");
  
}TEST_END

TEST_BEGIN("QuickSort")
{
  vector<int> input_data = get_random_data(1000, 500);
  vector<int> input_data_orig = get_copy(input_data);

  size_t size_before = input_data.size();
  quicksort(input_data, 0, (int) size_before-1);
  IsTrue("Correct Size", input_data.size() == size_before,
	 "Quicksort is changing the size of the input vector.");
  IsTrue("Contain Same Elements", vectors_contain_same(input_data, input_data_orig),
	 "Vectors do not contain the same data values.");
  IsTrue("Is Sorted", is_nondecreasing(input_data),
	 "Sorted vector is not actually sorted.");

}TEST_END

TEST_BEGIN("BubbleSort")
{
  vector<int> input_data = get_random_data(1000, 500);
  vector<int> input_data_orig = get_copy(input_data);

  size_t size_before = input_data.size();
  bubblesort(input_data);
  IsTrue("Correct Size", input_data.size() == size_before,
	 "Bubble Sort is changing the size of the input vector.");
  IsTrue("Contain Same Elements", vectors_contain_same(input_data, input_data_orig),
	 "Vectors do not contain the same data values.");
  IsTrue("Is Sorted", is_nondecreasing(input_data),
	 "Sorted vector is not actually sorted.");
  

}TEST_END

TEST_BEGIN("MergeSort")
{
  vector<int> input_data = get_random_data(1000, 500);
  vector<int> input_data_orig = get_copy(input_data);

  size_t size_before = input_data.size();
  mergesort(input_data);
  IsTrue("Correct Size", input_data.size() == size_before,
	 "Merge Sort is changing the size of the input vector.");
  IsTrue("Contain Same Elements", vectors_contain_same(input_data, input_data_orig),
	 "Vectors do not contain the same data values.");
  IsTrue("Is Sorted", is_nondecreasing(input_data),
	 "Sorted vector is not actually sorted.");
  

}TEST_END

TEST_BEGIN("MysterySort")
{
  
  vector<int> input_data = get_random_data(1000, 500);
  vector<int> input_data_orig = get_copy(input_data);

  size_t size_before = input_data.size();
  mystery_sort(input_data);
  IsTrue("Correct Size", input_data.size() == size_before,
	 "Mystery Sort is changing the size of the input vector.");
  IsTrue("Contain Same Elements", vectors_contain_same(input_data, input_data_orig),
	 "Vectors do not contain the same data values.");
  IsTrue("Is Sorted", is_nondecreasing(input_data),
	 "Sorted vector is not actually sorted.");

}TEST_END

SUITE_END

void printUsage(char call[]) {
  cout << " Usage: " << call << " [--retrograde]" << endl;
}

vector<int> get_random_data(int how_many, int upper_bound) {
  vector<int> numbers;
  for (int i=0; i < how_many; i++) {
    int r = rand() % upper_bound;
    numbers.push_back(r);
  }
  return numbers;
}

bool vector_contains(vector<int> &data, int value) {
  bool ret = false;
  for (size_t i = 0; i < data.size(); i++) {
    if (data[i] == value) {
      ret = true;
      break;
    }
  }
  return ret;
}

bool vectors_contain_same(vector<int>& blue, vector<int> &green) {
  bool ret = true;
  if (blue.size() != green.size()) {
    ret = false;
  } else {
    for (size_t i=0; i < blue.size(); i++) {
      int target = blue[i];
      bool found = vector_contains(green, target);
      if (!found) {
	ret = false;
	break;
      }
    }
  }
  return ret;
}

bool is_nondecreasing(vector<int>& data) {
  bool ret = true;
  if (data.size() > 1) {
    int prev = data[0];
    for (size_t i=1; i < data.size(); i++) {
      int here = data[i];
      if (prev > here) {
	ret = false;
	break;
      }
      prev = here;
    }
  }
  return ret;
}

vector<int> get_copy(vector<int> &data) {
  vector<int> ret;
  for (size_t i=0; i < data.size(); i++) {
    ret.push_back(data[i]);
  }
  return ret;
}

int main (int argc, char* argv[]) 
{
  // vector<int> data = get_random_data(100, 1000);
  // cout << "Got vector of size: " << data.size() << endl;
  // for (size_t i=0; i < data.size(); i++) {
  //   cout << data[i] << "\t";
  // }
  // cout << endl;
  // int missing = 0;
  // for (int i=0; i < 1000; i++) {
  //   if (vector_contains(data, i)) {
  //     cout << i << "\t";
  //   } else {
  //     missing++;
  //   }
  // }
  // cout << endl;
  // cout << "Missing " << missing << endl;

  if (argc == 2 && strcmp(argv[1], "--retrograde") == 0) RETROGRADE_MODE = 1;
  else if (argc != 1) { 
    printUsage(argv[0]);
    return -1;
  }
  
  UTFrameworkInit;
  
}
