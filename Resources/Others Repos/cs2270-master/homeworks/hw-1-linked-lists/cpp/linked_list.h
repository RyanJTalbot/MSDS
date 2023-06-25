/*

  linked_list.h

 */

#ifndef __linked_list__
#define __linked_list__

#include <iostream>
#include <string>

// this is the basic node structure for a linked list.
struct node {
  int data;    // data: the value of this node
  node* next;  // next: pointer to the next node in the list, or NULL
	       // if this is the last node.
};

// create a new node structure that points to NULL and holds the
// provided integer. return a pointer to that new node.
node* init_node(int data);

// create a space-separated string representing the contents of the
// list, in the same order they are found beginning from the head of
// the list. return that string object.  For example, this might
// return "" (the empty string) if the list is empty, or it might
// return "1 7 3" or "1 7 3 " (note the space at the end, you can have
// that there and it is OK).
std::string report(node* head);

// insert an integer into the list pointed to by head. the resulting
// list is one element longer, and the newly appended node has the
// given data value. consider using the 'append' function to help.
void append_data(node** head, int data);

// this is the same as append_data, except we're adding a node, rather
// than a value. 
void append(node** head, node* new_node);

// similar to append_data. insert a new node that contains the given
// data value, such that the new node occupies the offset
// indicated. Any nodes that were already in the list at that offset
// and beyond are shifted down by one. For example if the list
// contains 23, 74, 93, and we insert 42 at index 1, the resulting
// list should be 23, 42, 74, 93.
void insert_data(node** head, int offset, int data);

// this is the same as insert_data, except we're inserting a node,
// rather than a value.
void insert(node** head, int offset, node* new_node);

// remove the node indicated by the given offset. For example if our
// list contains 23, 74, 93, and we remove offset 1, the resulting
// list should then contain 23, 93.
void remove(node** parent, int offset);

// report the number of nodes in the linked list pointed to by head.
int size(node* head);

// return true if the linked list pointed to by head contains a node
// with the specified value.
bool contains(node* head, int data);

#endif /* defined __linked_list__ */
