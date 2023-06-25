#include <iostream>
#include "deque.h"

using namespace std;

deque* init_deque( ) {
  deque* ret = new deque();
  ret->start = NULL;
  ret->end = NULL;
  return ret;
}

node* init_node( int val ) {
  node* ret = new node();
  ret->prev = NULL;
  ret->next = NULL;
  ret->value = val;
  return ret;
}

void push (deque* &queue, int val) {
  if (queue->end == NULL && queue->start == NULL) {
    node* n = init_node(val);
    queue->start = n;
    queue->end = n;
    n->value = val;
  } else {

  }
}

void push_front (deque* &queue, int val) {

}

int pop ( deque* &queue ) {

}

int pop_front ( deque* &queue ) {

}

int peek ( deque* &queue ) {

}

int peek_front ( deque* &queue ) {

}

int size ( deque* &queue ) {

}

bool contains (deque* &queue, int val) {

}
