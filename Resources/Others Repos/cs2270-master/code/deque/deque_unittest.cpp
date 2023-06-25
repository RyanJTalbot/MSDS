/*

  deque_unittest.cpp

*/

#include <cstring>
#include <cstdlib>
#include "deque.h"
#include "UTFramework.h"

using namespace Thilenius;
using namespace std;

extern int RETROGRADE_MODE;

/* begin a suite. This is a collection of tests. */

SUITE_BEGIN("Deque")     

/* now define tests with the same form as the sanity check. */

TEST_BEGIN("Sanity Check") {
  IsTrue("Sane?",        // label in output
	 true,           // a truth test
	 "I'm insane!"); // error message when needed
}TEST_END

TEST_BEGIN("Init Deque") {
  deque* q = init_deque();

  IsTrue("Init Not Null?",        // label in output
	 q != NULL,              // a truth test
	 "It isn't ok!"); // error message when needed

  // q->start and q-> end must be null to start with
IsTrue("Init Start End Null?",        // label in output
	 q->start == NULL,              // a truth test
	 "It isn't ok!"); // error message when needed

  IsTrue("Init End Null?",        // label in output
	 q->end == NULL,              // a truth test
	 "It isn't ok!"); // error message when needed
  
}TEST_END

TEST_BEGIN("Init Node") {
  node* n = init_node( 10 );
  IsTrue("Is it Null?",        // label in output
	 n != NULL,           // a truth test
	 "It is null :("); // error message when needed

  IsTrue("Value ok?",
	 n->value == 10,
	 "It isn't returning the right value.");

  IsTrue("Next ok?",
	 n->next == NULL,
	 "It should be NULL");

  IsTrue("Prev ok?",
	 n->prev == NULL,
	 "It should be NULL");
}TEST_END

TEST_BEGIN("Insert") {
deque* q = init_deque();
push(q, 10);

  IsTrue("Push onto Empty",        // label in output
	   q->start != NULL,           // a truth test
	 "Start should not be null"); // error message when needed

  IsTrue("Push onto Empty",        // label in output
	   q->end != NULL,           // a truth test
	 "End should not be null"); // error message when needed

  IsTrue("Push onto Empty",        // label in output
	   q->start->value == 10,           // a truth test
	 "First value is not correct."); // error message when needed


}TEST_END

 /* end the suite, since all of this was a macro definition. */

SUITE_END

 /* the below is just a main function to get the unit test started. */
void printUsage(char call[]) {
  cout << " Usage: " << call << " [--retrograde]" << endl;
}

int main (int argc, char* argv[]) {
  if (argc == 2 && strcmp(argv[1], "--retrograde") == 0) RETROGRADE_MODE = 1;
  else if (argc != 1) { 
    printUsage(argv[0]);
    return -1;
  }
  UTFrameworkInit;
}
