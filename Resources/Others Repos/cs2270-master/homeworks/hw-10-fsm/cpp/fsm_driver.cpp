/*
   fsm_driver.cpp

   No arguments gives you the pretty colorized mode:

   ./fsm_driver.cpp

   The "--manual" argument causes the 'manual' function to run instead
   of running any of the unit test code:

   ./fsm_driver --manual

   The "--retrograde" argument causes the driver to run exacly as it
   does on the server:

   ./fsm_driver --retrograde

   Feel free to edit this file's manual() function to run your own
   testing. I have some stuff there to start with, you can use that or
   not, it is up to you.

 */
#include "fsm.hpp"

using namespace Thilenius;
using namespace std;

FSM fsm_simple() {
  FSM fsm;
  int even = fsm.addState("Even", true);
  int odd = fsm.addState("Odd");
  fsm.addTransition(even, even, 1, "1");
  fsm.addTransition(even, odd, 0, "0");
  fsm.addTransition(odd, odd, 1, "1");
  fsm.addTransition(odd, even, 0, "0");
  return fsm;
}

FSM fsm_moonman() {
  FSM fsm;
  int start = fsm.addState("No Input");
  int bogus = fsm.addState("Not MOONMAN");
  int m1 = fsm.addState("M");
  int o1 = fsm.addState("O"); 
  int o2 = fsm.addState("O");
  int n1 = fsm.addState("N");
  int m2 = fsm.addState("M");
  int a1 = fsm.addState("A");
  int n2 = fsm.addState("N", true);
  
  fsm.addTransition(start, m1, (int) 'M', "M"); // 1
  fsm.addTransition(m1, o1, (int) 'O', "O");    // 2
  fsm.addTransition(o1, o2, (int) 'O', "O");    // 3
  fsm.addTransition(o2, n1, (int) 'N', "N");    // 4
  fsm.addTransition(n1, m2, (int) 'M', "M");    // 5
  fsm.addTransition(m2, a1, (int) 'A', "A");    // 6
  fsm.addTransition(a1, n2, (int) 'N', "N");    // 7

  fsm.addTransition(start, bogus, (int) 'X', "X"); // 8
  fsm.addTransition(m1, bogus, (int) 'X', "X"); // 9
  fsm.addTransition(o1, bogus, (int) 'X', "X"); // 10
  fsm.addTransition(o2, bogus, (int) 'X', "X"); // 11
  fsm.addTransition(n1, bogus, (int) 'X', "X"); // 12
  fsm.addTransition(m2, bogus, (int) 'X', "X"); // 13
  fsm.addTransition(a1, bogus, (int) 'X', "X"); // 14
  fsm.addTransition(n2, bogus, (int) 'X', "X"); // 15
  
  return fsm;
}

FSM fsm_brain_bag() {
  FSM fsm;
  int S  = fsm.addState("Start State");
  int Z  = fsm.addState("Bogus State");
  int b  = fsm.addState("B");
  int i  = fsm.addState("I");
  int r  = fsm.addState("R");
  int a  = fsm.addState("A");
  int n  = fsm.addState("N", true);
  int g  = fsm.addState("G", true);
  int a2 = fsm.addState("A", true);
  int s  = fsm.addState("S", true);
  int i2 = fsm.addState("I");
  int n2 = fsm.addState("N", true);
  fsm.addTransition(S, b, (int) 'B', "B");
  fsm.addTransition(b, i, (int) 'I', "I");
  fsm.addTransition(b, r, (int) 'R', "R");
  fsm.addTransition(b, a, (int) 'A', "A");
  fsm.addTransition(i, n, (int) 'N', "N");
  fsm.addTransition(i, g, (int) 'G', "G");  
  fsm.addTransition(r, a2, (int) 'A', "A");
  fsm.addTransition(a, g, (int) 'G', "G");
  fsm.addTransition(n, s, (int) 'S', "S");
  fsm.addTransition(a2, s, (int) 'S', "S");
  fsm.addTransition(a2, i2, (int) 'I', "I");
  fsm.addTransition(i2, n2, (int) 'N', "N");
  fsm.addTransition(n2, s, (int) 'S', "S");
  fsm.addTransition(S, Z, -1, "Bogus");
  fsm.addTransition(b, Z, -1, "Bogus");
  fsm.addTransition(i, Z, -1, "Bogus");
  fsm.addTransition(r, Z, -1, "Bogus");
  fsm.addTransition(a, Z, -1, "Bogus");
  fsm.addTransition(n, Z, -1, "Bogus");
  fsm.addTransition(g, Z, -1, "Bogus");
  fsm.addTransition(a2, Z, -1, "Bogus");
  fsm.addTransition(s, Z, -1, "Bogus");
  fsm.addTransition(i2, Z, -1, "Bogus");
  fsm.addTransition(n2, Z, -1, "Bogus");
  return fsm;
}

/**
 * In case you are curious: this treats the FSM like a recognizer. It
 * resets the FSM to a default state and then processes each character
 * in the input string. If at the end of the string it is in an
 * accepting state, it means the FSM matched that string.
 *
 * the 'exp' param tells us if we actually expect it to recognize it.
 *
 * the 'is_bogus' param tells us if we expect the FSM to go into a
 * terminally bogus state, meaning it absolutely won't recognize the
 * input, no matter what comes next.
 *
 * It is possible for it to be in an unaccepted state without being
 * bogus. For example the string "BA" is not accepted, but if the next
 * character is "G", then the FSM would be in an accepted state.
 **/
void recognize(FSM& fsm, string input, bool exp, bool is_bogus) {
  fsm.setState(fsm.getDefaultState());
  State* st;
  st = fsm.getState(fsm.getCurrentState());
  if (st == NULL) {
    IsTrue("Null", false, "Current State is NULL");
    return;
  }
  //  cout << "Initial state: " << st << endl;
  string::iterator it = input.begin(); 
  for(; it != input.end(); it++) {
    char c = *it;
    int sig = (int) c;
    fsm.handleSignal(sig);
    st = fsm.getState(fsm.getCurrentState());
    //    cout << "After " << c << ", current state: " << st << endl;
  }
  IsTrue(input, fsm.isAcceptState() == exp, "Wrong Accept State"); 
  if (is_bogus) {
    st = fsm.getState(fsm.getCurrentState());
    IsTrue("Bogus", st->label == "Bogus State", "Should be in Bogus state");
  }
}

void manual() {
  // to run the manual tester just run
  // ./fsm_driver --manual

  cout << "Manual Program Begin" << endl;
  char a = 'A';
  int a_as_int = (int) a;
  cout << a << " vs " << a_as_int << endl;
  cout << 'B' << " vs " << (int) 'B' << endl;
  cout << "Manual Program End" << endl;
}

SUITE_BEGIN("Finite State Machines")

TEST_BEGIN("Defaults")
{
  FSM fsm;
  int current = fsm.getCurrentState();
  IsTrue("Current State", current == -1, "Default current state should be -1");
  bool accept = fsm.isAcceptState();
  IsTrue("Accept", accept == false, "Default accept state should be false");
  State* bogus = fsm.getState(0);
  IsTrue("State", bogus == NULL, "Default getState should give NULL");
  int defstate = fsm.getDefaultState();
  IsTrue("DefState", defstate == -1, "Default default state should be -1");
  bool handle = fsm.handleSignal(0);
  IsTrue("Handle Signal", handle == false, 
	 "Default fsm should not be able to handle signals");
  bool numStates = fsm.countStates();
  IsTrue("NumStates", numStates == 0, "Default num states should be 0");
  bool numTrans = fsm.countTransitions();
  IsTrue("NumTrans", numTrans == 0, "Default num transitions should be 0");
}TEST_END

TEST_BEGIN("Add States")
{
  FSM fsm;
  int even = fsm.addState("even", true);
  int odd = fsm.addState("odd");
  IsTrue("Non-Negative IDs", (even >= 0 && odd >= 0), 
	 "FSM assigned negative ID to state");
  IsTrue("Non-equal IDs", even != odd, "FSM assigned same ID to two states");
  int current = fsm.getCurrentState();
  IsTrue("Current State", current == even, "Current state is wrong");
  bool accept = fsm.isAcceptState();
  IsTrue("Accept", accept, "Accept state should be true");
  fsm.setState(odd);
  current = fsm.getCurrentState();
  IsTrue("Current State", current == odd, "Current state is wrong");
  accept = fsm.isAcceptState();
  IsTrue("Accept", !accept, "Accept state should be false");
  int count = fsm.countStates();
  IsTrue("Count States", count == 2, "There are two states");
}TEST_END

TEST_BEGIN("Add Transitions")
{
  // this assuments everything in the AddStates test works
  FSM fsm;
  int start = fsm.addState("No Input");
  int m1 = fsm.addState("M");
  int o1 = fsm.addState("O"); 
  int o2 = fsm.addState("O");
  int n1 = fsm.addState("N");
  int m2 = fsm.addState("M");
  int a1 = fsm.addState("A");
  int n2 = fsm.addState("N", true);
  
  int start_tr = fsm.addTransition(start, m1, (int) 'M', "M"); // 1
  Transition* tr = fsm.getTransition(start_tr);
  IsTrue("Null", tr != NULL, "Transition just added is NULL");
  if (tr != NULL) {
    IsTrue("Signal", tr->signal == (int) 'M', "Signal not recorded");
    IsTrue("Label", tr->label == "M", "Label not recorded");
    fsm.addTransition(m1, o1, (int) 'O', "O");    // 2
    fsm.addTransition(o1, o2, (int) 'O', "O");    // 3
    fsm.addTransition(o2, n1, (int) 'N', "N");    // 4
    fsm.addTransition(n1, m2, (int) 'M', "M");    // 5
    fsm.addTransition(m2, a1, (int) 'A', "A");    // 6
    fsm.addTransition(a1, n2, (int) 'N', "N");    // 7

    int num_trans = fsm.countTransitions();
    IsTrue("Count Transitions", num_trans == 7, "Wrong number of transitions");

    // now add some transitions that it should reject
    fsm.addTransition(-1, n2, (int) 'X', "X"); // still 7
    num_trans = fsm.countTransitions();
    IsTrue("Count Transitions", num_trans == 7, "Wrong number of transitions");
    fsm.addTransition(n1, m2, (int) 'M', "M"); // still 7
    num_trans = fsm.countTransitions();
    IsTrue("Count Transitions", num_trans == 7, "Wrong number of transitions");  
  }
}TEST_END

TEST_BEGIN("Simple Signals")
{
  FSM fsm = fsm_simple(); // accepts even numbers of zeros
  int def = fsm.getDefaultState();
  State* st;
  bool went;
  bool acc;
  went = fsm.handleSignal(1);
  IsTrue("Trans Followed", went, "Should transition on signal");
  IsTrue("Accepting", fsm.isAcceptState(), "Accept state wrong");
  went = fsm.handleSignal(0);
  IsTrue("Trans Followed", went, "Should transition on signal");
  IsTrue("Accepting", !fsm.isAcceptState(), "Accept state wrong");
  fsm.setState(fsm.getDefaultState());
  IsTrue("Reset", fsm.getCurrentState() == def, "Reset to Default wrong");
  acc = fsm.isAcceptState();
  IsTrue("Accepting", acc, "Accept state wrong");
  bool trial_ok = true;
  for (int i=0; i< 3; i++) {
    fsm.handleSignal(0);
    if (acc == fsm.isAcceptState()) {
      IsTrue("Accepting", acc == fsm.isAcceptState(), "Accept state wrong");
      trial_ok = false;
      break;
    }
    acc = fsm.isAcceptState();
  }
  if (trial_ok) {
    IsTrue("Zeros", trial_ok, "Trial for zeros OK");
  }
  fsm.setState(fsm.getDefaultState());
  acc = fsm.isAcceptState();
  trial_ok = true;
  for (int i=0; i< 3; i++) {
    fsm.handleSignal(1);
    if (acc != fsm.isAcceptState()) {
      IsTrue("Accepting", acc != fsm.isAcceptState(), "Accept state wrong");
      trial_ok = false;
      break;
    }
    acc = fsm.isAcceptState();
  }
  if (trial_ok) {
    IsTrue("Ones", trial_ok, "Trial for ones OK");
  }
  went = fsm.handleSignal(42);
  IsTrue("Bogus Signal", !went, "Shouldn't go anywhere for that input");
}TEST_END

TEST_BEGIN("MOONMAN")
{
  FSM moonman = fsm_moonman();
  State* st;
  moonman.handleSignal((int) 'M');
  IsTrue("Accepting", !moonman.isAcceptState(), "Shouldn't accept yet");
  st = moonman.getState(moonman.getCurrentState());
  IsTrue("Null", st != NULL, "Current state pointer is NULL");
  moonman.handleSignal((int) 'O');
  moonman.handleSignal((int) 'O');
  moonman.handleSignal((int) 'N');
  moonman.handleSignal((int) 'M');
  moonman.handleSignal((int) 'A');
  moonman.handleSignal((int) 'N');
  IsTrue("Accepting", moonman.isAcceptState(), "Should accept now");
  st = moonman.getState(moonman.getCurrentState());
  IsTrue("Null", st != NULL, "Current state pointer is NULL");
  moonman.setState(moonman.getDefaultState());
  IsTrue("Accepting", !moonman.isAcceptState(), "Shouldn't accept yet");
  bool went;
  went = moonman.handleSignal((int) 'Q');
  IsTrue("Went", !went, "Should not transition on weirdo signals");
  went = moonman.handleSignal((int) 'N');
  IsTrue("Went", !went, "Should not transition on weirdo signals");
  went = moonman.handleSignal((int) '#');
  IsTrue("Went", !went, "Should not transition on weirdo signals");
  IsTrue("Accepting", !moonman.isAcceptState(), "Shouldn't accept yet");
  
}TEST_END

TEST_BEGIN("BRAIN BAG")
{
  FSM brain_bag = fsm_brain_bag();
  recognize(brain_bag, "MONKEY", false, true);
  recognize(brain_bag, "BIN", true, false);
  recognize(brain_bag, "BINS", true, false);
  recognize(brain_bag, "BA", false, false);
  recognize(brain_bag, "BAA", false, true);
  recognize(brain_bag, "BRAIN", true, false);
  recognize(brain_bag, "BRAINS", true, false);
  recognize(brain_bag, "BUS", false, true);
}TEST_END

SUITE_END

int main (int argc, char* argv[])
{	
  if (argc == 2 && argv[1] == string("--manual")) {
    manual();
  } else {
    UTFrameworkInit;
  }
}
