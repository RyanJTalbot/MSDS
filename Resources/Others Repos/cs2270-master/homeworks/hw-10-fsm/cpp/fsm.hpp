#ifndef __fsm_h__
#define __fsm_h__

#include <string>
#include <iostream>
#include <vector>
#include <iostream>

#include "UTFramework.h"

#define FAILURE_SIGNAL -1

using namespace std;

// forward declarations
class State;
class Transition;

class FSM {
private:

  vector<State*> states; // I recommend you use the index for state IDs

  vector<Transition*> transitions; // Same thing with transitions

  int state; // the current state of the FSM. Default should be -1

  int default_state; // default state of the FSM. Default should be
		     // -1. This can be used to reset the FSM with
		     // setState(getCurrentState()).

public:

  /**
   * Implement the constructor to initialize some variables as
   * described above.
   **/
  FSM();

  /**
   * Adds a state with the given label. The is_accept_state parameter
   * tells us if this is an 'acceptable' state. Be sure to initialize
   * the failure_trans to -1.
   *
   * The state is installed in the FSM and given a non-negative
   * integer id that is unique among states. That id is returned.
   *
   * If this is the first state added to the FSM, the FSM enters this
   * state and sets the default state to the new state id. 
   **/
  int addState(string label, bool is_accept_state);

  /**
   * Adds a state with the given label. This is equivalent to
   * addState(label, false). See the other addState function for
   * remaining documentation.
   **/
  int addState(string label);

  /**
   * Adds a transition between two states that activates when the
   * given signal is received. This is considered duplicate if there
   * is another transition from stateA to stateB with the same
   * signal. The transition label is ignored when determining
   * duplicate status. 
   * 
   * If this is a duplicate, nothing is done and -1 is returned. 
   *
   * If either state is not present in the FSM, nothing is done and -1
   * is returned.
   *
   * Otherwise, a new transition is installed in the FSM and given a
   * non-negative id that is unique among transitions. That id is
   * returned.
   *
   * stateA: the start state's id. The FSM must be in this state for
   *         the transition to take place.
   *
   * stateB: the end state. After taking the transition, the FSM will
   *         be placed in stateB.
   *
   * signal: the signal that (assuming we are in stateA) will trigger
   *         this particular transition. If the signal is
   *         FAILURE_SIGNAL, it is considered the 'failure signal',
   *         which is a catch-all for bad input. If this is the
   *         failure signal, stateA will use this transition if it
   *         receives a signal that it can not otherwise use.
   *
   * transLabel: the label for this transition. 
   **/
  int addTransition(int stateA, int stateB, 
		    int signal, string transLabel);

  /**
   * Returns the number of states this FSM has.
   **/
  int countStates();

  /**
   * Returns the number of transitions this FSM has.
   **/
  int countTransitions();

  /**
   * Returns the FSM's current state, or -1 if the FSM has no current
   * state.
   **/
  int getCurrentState();

  /**
   * Returns true if the current state is 'acceptable', false otherwise.
   **/
  bool isAcceptState();

  /**
   * Returns a pointer to the State object with the given id, or NULL
   * if no such state is in the FSM.
   **/
  State* getState(int id);

  /**
   * Returns a pointer to the Transition object with the given id, or
   * NULL if no such transition is in the FSM.
   **/
  Transition* getTransition(int id);

  /**
   * Return the id of the default state for this FSM. If there is no
   * default state this returns -1.
   **/
  int getDefaultState();

  /**
   * Sets the state to the given value. The default state is the first
   * state that was added to the FSM.
   **/
  void setState(int id);

  /**
   * Handle an input event signal. For the current state, this should
   * be compared to each possible transition's signal. If there is
   * match, that transition is taken and the FSM enters the state on
   * the other end of the transition. 
   *
   * If no regular transition was taken, and if the current state has
   * a nonzero ID for a failure transition, that transition should be
   * used.
   *
   * If a transition was taken, return true. Otherwise return false.
   **/
  bool handleSignal(int signal);

}; // end class FSM

class State {
public:
  bool accept;  // true if the state is an 'accepting' state

  string label; // state's text label. Used by driver to sanity check.

  int failure_trans; // if non-negative, this is the transition used
		     // when we receive a signal while in this state
		     // but don't have any matching transitions in the
		     // 'trans' vector for the input signal.

  vector<int> trans; // normal transition ids are stored here.

  friend ostream &operator << (ostream& out, State* state);
};

class Transition {
public:
  string label;   // label for this transition. a debugging var.
  int signal;     // signal this transition reacts to
  int next_state; // id of the state we transition to when activated
};

#endif

