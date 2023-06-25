//
// binary_search_tree.h
//
#include <iostream>
#include <vector>

struct bt_node {
  int data;
  bt_node* left;
  bt_node* right;
};

/**
 * Initialize a bt_node with the given data, and two NULL children.
 */
bt_node* init_node(int data);

/**
 * Insert the new_node in a proper location in the tree indicated by
 * *top_ref. On return, *top_ref points to the root of the tree.
 */
void insert(bt_node** top_ref, bt_node* new_node);

/**
 * Insert a new node with the given data value similarly to insert().
 */
void insert_data(bt_node** top_ref, int data);

/**
 * Removes a node from the tree whose data value is the same as the
 * input. On return, *top_ref points to the root of the tree. If no
 * node in the tree contains the given data, this function has no
 * effect.
 */
void remove(bt_node** top_ref, int data);

/**
 * Return true if any node in the tree pointed to by top contains the
 * given data value.
 */
bool contains(bt_node* top, int data);

/**
 * Searches through the tree pointed to by top for a node that
 * contains the given data value. If such a node is found, a pointer
 * to it is returned. Otherwise this function returns NULL.
 */
bt_node* get_node(bt_node* top, int data);

/**
 * Return the size of the tree pointed to by top. In other words, it
 * returns the number of nodes that are reachable by traversing the
 * tree pointed to by top. If the tree is empty (top is NULL), it
 * returns zero.
 */
int size(bt_node* top);

/**
 * Fill an integer array to reflect the contents of this binary
 * tree. The filled array will be the same as the tree's size (found
 * with the size() function), and the order of the array elements are
 * the same that is found during an inorder traversal of the tree.
 *
 * Note: the array is created and sized before this function is
 * called. You will have at least size(top) elements available, so you
 * may safely index [0..size(top)-1].
 */
void to_array(bt_node* top, int arr[]);



