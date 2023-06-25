#ifndef __linked_list_h__
#define __linked_list_h__

#include <iostream>

class LinkedListNode {
public:
  LinkedListNode(int data);
  LinkedListNode(); // constructor
  ~LinkedListNode(); // destructor
  int value;
  LinkedListNode* next;
};

/**
 * The LinkedList class encapsulates the data and operations for a
 * simple linked list of integers. We use it via the public interface.
 **/
class LinkedList {

  // ------------------------------------------ private members
private:

  LinkedListNode* root;

  // ------------------------------------------- public members
public:
  
  LinkedList();

  const std::string report();

  void append(int data);
  
  void insert(int data, int offset);

  void remove(int offset);

  int size();

  bool contains(int data);

  friend std::ostream &operator << (std::ostream& out, LinkedList list);

}; // you have to have a semicolon at the end.

#endif
