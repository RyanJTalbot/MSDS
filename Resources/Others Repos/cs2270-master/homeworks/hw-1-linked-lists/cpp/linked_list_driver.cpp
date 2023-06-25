#include <iostream>
#include "linked_list.h"

using namespace std;

int main () {
  cout << "Testing Linked List" << endl;
  node* empty_list = NULL; // empty list
  cout << "Empty List Contents: " << report(empty_list) << endl; // should be ''
  append_data(&empty_list, 16);
  cout << "Empty List Contents after appending 16: " 
       << report(empty_list) << endl; // should be '16'

  // now lets make a proper list that we manipulate
  node* head = init_node(5);
  cout << "Initial List Contents: " << report(head) << endl; // should be '5'
  // append a number
  append_data(&head, 42);
  cout << "After adding 42: " << report(head) << endl; // should be '42'
  // append a few more
  append_data(&head, 32);
  append_data(&head, 99);
  cout << "Should be 5, 42, 32, 99: " << report(head) << endl;
  // Now try appending nodes
  node* seven = init_node(7);
  node* ten = init_node(10);
  append(&head, seven);
  append(&head, ten);
  cout << "Added 7 and 10: " << report(head) << endl;

  // As you can see, for function calls that take a node*, such as
  // report, we just pass in a node* directly.

  // For functions that take a node** (that's a pointer-to-a-pointer),
  // we need to use the address-of operator, the ampersand. So,
  // append(&head, child) is right.

  // This should give you a good starting point to fill in the rest of
  // this driver. Writing a good testing program is an art. Remember
  // that there are many functions to write, meaning you should
  // consider writing lots of code here (or even test functions) that
  // tests them.
}
