/*

  fsm.cpp - Finite State Machine

  Read the header file 'fsm.hpp' for all documentation on individual
  functions. I suggest you start by getting the unit test cases to
  pass in order. E.g. start with the Defaults one, then do Add States,
  and so on.

  Your Name: 

  Your Collaborators:

 */

#include "fsm.hpp"

using namespace std;

FSM::FSM() {
  // implement me
}

int FSM::addState(string label, bool is_accept_state) {
  // implement me
  return -1;
}

int FSM::addState(string label) {
  // implement me

  return -1;
}

int FSM::addTransition(int stateA, int stateB, 
		       int signal, string transLabel) {
  // implement me
  return -1;
}

int FSM::countStates() {
  // implement me
  return -1;
}

int FSM::countTransitions() {
  // implement me
  return -1;
}

int FSM::getCurrentState() {
  // implement me
  return 0;
}

bool FSM::isAcceptState() {
  // implement me
  return false;
}

State* FSM::getState(int id) {
  // implement me
  return NULL;
}

Transition* FSM::getTransition(int id) {
  // implement me
  return NULL;
}

int FSM::getDefaultState() {
  // implement me
  return 0;
}

void FSM::setState(int id) {
  // implement me
}

bool FSM::handleSignal(int signal) {
  // implement me
  return false;
}

ostream &operator << (ostream& out, State* st) {
  if (st == NULL) {
    out << "State: NULL";
  } else {
    out << "State: " << st->label;
    if (st->accept) {
      out << " +";
    }
  }
  return out;
}
