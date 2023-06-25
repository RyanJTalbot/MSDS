/*

  deque.h

  Define functions for double ended queue.

*/

struct node {
  node* prev;
  node* next;
  int value;
};

struct deque {
  node* start;
  node* end;
};

deque* init_deque( );

node* init_node( int val );

void push (deque* &queue, int val);

void push_front (deque* &queue, int val);

int pop ( deque* &queue );

int pop_front ( deque* &queue );

int peek ( deque* &queue );

int peek_front ( deque* &queue );

int size ( deque* &queue );

bool contains (deque* &queue, int val);
