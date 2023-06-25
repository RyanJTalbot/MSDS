#include <iostream>
#include <sstream>
#include "LinkedList.hpp"

using namespace std;

// this file implements all the functions (public and private) defined
// in the header file. They are all prefixed with 'LinkedListNode::'
// before the identifier so the functions are associated with the
// LinkedListNode and LinkedList class.

LinkedListNode::LinkedListNode(int data) {
  cout << "  >> LinkedListNode(" << data << ")" << endl;
  value = data;
  next = NULL;
}

LinkedListNode::LinkedListNode() {
  cout << "  >> LinkedListNode()" << endl;
}

LinkedListNode::~LinkedListNode() {
  cout << "  >> ~LinkedListNode() (destructor)" << endl;
}

LinkedList::LinkedList() {
  cout << "  >> Creating LinkedList instance." << endl;
  root = NULL;
}

const string LinkedList::report() {
  stringstream ss;
  if (root != NULL) {
    ss << "[ ";
    LinkedListNode* cursor = root;
    while (cursor != NULL) {
      ss << cursor->value << ", ";
      cursor = cursor->next;
    }
    ss << "]";
  }
  return ss.str();
}

void LinkedList::append(int data)  {
  cout << "  >> append(" << data << ")" << endl;
  if (root == NULL) {
    root = new LinkedListNode(data);
  } else {
    LinkedListNode* cursor = root;
    while (cursor->next != NULL) {
      cursor = cursor->next;
    }
    cursor->next = new LinkedListNode(data);
  }
}
  
void LinkedList::insert(int data, int offset) {
  cout << "  >> insert(" << data << ", " << offset << ")" << endl;
  if (offset < 0) {
    // ignore
  } else if (offset == 0) {
    LinkedListNode* new_root = new LinkedListNode(data);
    LinkedListNode* old_root = root;
    root = new_root;
    root-> next = old_root;
  } else {
    LinkedListNode* cursor = root;
    for (int i=1; i < offset; i++) {
      if (cursor == NULL) {
	break;
      }
      cursor = cursor->next;
    }
    if (cursor != NULL) {
      LinkedListNode* new_node = new LinkedListNode(data);
      LinkedListNode* next = cursor->next;
      cursor->next = new_node;
      new_node->next = next;
    }
  }
}

void LinkedList::remove(int offset) {
  cout << "  >> remove(" << offset << ")" << endl;  
  if (offset < 0) {
    // ignore
  } else if (offset == 0 && root != NULL) {
    // replace root
    root = root->next;
  } else {
    LinkedListNode* cursor = root;
    for (int i=1; i < offset; i++) {
      if (cursor == NULL) {
	break;
      }
      cursor = cursor->next;
    }
    if (cursor != NULL && cursor->next != NULL) { 
      // cursor is one before the doomed. route around it.
      LinkedListNode* doomed = cursor->next;
      cursor->next = cursor->next->next;
      delete doomed;
    }
  }
}

int LinkedList::size() {
  cout << "  >> size()" << endl;  
  int ret = 0;
  LinkedListNode* cursor = root;
  while (cursor != NULL) {
    ret = ret + 1;
    cursor = cursor->next;
  }
  return ret;
}

bool LinkedList::contains(int data) {
  cout << "  >> contains(" << data << ")" << endl;  
  bool ret = false;
  LinkedListNode* cursor = root;
  while (cursor != NULL) {
    if (cursor->value == data) {
      ret = true;
      break;
    }
    cursor = cursor->next;
  }
  return ret;
}

ostream &operator << (ostream& out, LinkedList list) {
  if (list.root != NULL) {
    out << "[ ";
    LinkedListNode* cursor = list.root;
    while (cursor != NULL) {
      out << cursor->value << ", ";
      cursor = cursor->next;
    }
    out << "]";
  }
  return out;
}

int main() {
  cout << "Starting LinkedList object demo." << endl;
  LinkedList list; 
  list.append(42);
  cout << list << endl;
  list.append(84);
  cout << list << endl;
  list.append(243);
  cout << list << endl;
  list.append(-18);
  cout << list << endl;
  list.append(0);
  cout << list << endl;
  list.insert(40, 0);
  cout << list << endl;
  list.insert(41, 0);
  cout << list << endl;
  list.insert(42, 0);
  cout << list << endl;
  list.insert(23, 5);
  cout << list << endl;
  list.remove(1);  
  cout << list << endl;
  list.remove(0);
  cout << list << endl;
  list.append(100);
  cout << list << endl;
  cout << "contains 40? " << endl;
  cout << list.contains(40) << endl;
  cout << "contains 900? " << endl;
  cout << list.contains(900) << endl;
  cout << "size: " << endl;
  cout << list.size() << endl;
  cout << "final list contents: " << endl;
  cout << list << endl;
  cout << "string representation is: " << endl;
  cout << list.report() << endl;
  
  return 0;
}
