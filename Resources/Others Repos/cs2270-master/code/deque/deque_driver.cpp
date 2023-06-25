#include <iostream>
#include "deque.h"

using namespace std;

int main( ) {
  cout << "Word up, CSCI 2270." << endl;

  deque* queue = init_deque();
  cout << "My queue is: " << queue << endl;
  cout << "The start and end are: " << queue->start 
       << " and " << queue->end << endl;
  
  
}
