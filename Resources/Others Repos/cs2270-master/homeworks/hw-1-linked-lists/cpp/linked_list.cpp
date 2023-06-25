/*

  linked_list.cpp

  <document your work here: explain what it does from a high level.>

 */

// AUTHOR: <Your name here. Don't include student ID>

// WHAT: CSCI 2270 Assignment 1

// COLLABORATORS: <List of EVERYBODY you worked with, including
// instructors, TAs, and other students. Include people you helped.>

// <List of EVERY WEB SITE you consulted substantially> <Don't worry!
// Collaboration is encouraged. This is not cheating.>

// include the header file that provides function prototypes and the
// node structure. When you turn in your assignment, the grading
// system will use its own copy of this file, so don't edit it, and
// implement all the functions it specifies.
#include "linked_list.h"

// sstream gives you the stringstream object. Google it, and admire
// how much easier this makes life.
#include <sstream>

using namespace std;


// your linked list implementation goes here :)

// create a new node structure that points to NULL and holds the
// provided integer. return a pointer to that new node.
node* init_node(int data) {
  return NULL; // change this to return a newly initialized node.
}

// create a space-separated string representing the contents of the
// list, in the same order they are found beginning from the head of
// the list. return that string object.  For example, this might
// return "" (the empty string) if the list is empty, or it might
// return "1 7 3" or "1 7 3 " (note the space at the end, you can have
// that there and it is OK).
std::string report(node* root) {
  return NULL; // change this to return a proper string, 
               // even if it is a zero-length string object.
}

// insert an integer into the list pointed to by head. the resulting
// list is one element longer, and the newly appended node has the
// given data value. consider using the 'append' function to help.
void append_data(node** head, int data) {
  // implement me
}

// this is the same as append_data, except we're adding a node, rather
// than a value. 
void append(node** head, node* new_node) {
  // implement me
}

// similar to append_data. insert a new node that contains the given
// data value, such that the new node occupies the offset
// indicated. Any nodes that were already in the list at that offset
// and beyond are shifted down by one. For example if the list
// contains 23, 74, 93, and we insert 42 at index 1, the resulting
// list should be 23, 42, 74, 93.
void insert_data(node** head, int offset, int data) {
  // implement me
}

// this is the same as insert_data, except we're inserting a node,
// rather than a value.
void insert(node** head, int offset, node* new_node) {
  // implement me
}

// remove the node indicated by the given offset. For example if our
// list contains 23, 74, 93, and we remove offset 1, the resulting
// list should then contain 23, 93.
void remove(node** parent, int offset) {
  // implement me
}

// report the number of nodes in the linked list pointed to by head.
int size(node* head) {
  return 0; // implement me
}

// return true if the linked list pointed to by head contains a node
// with the specified value.
bool contains(node* head, int data) {
  return false; // implement me
}
