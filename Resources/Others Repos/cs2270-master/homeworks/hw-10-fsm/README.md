Finite State Machines
=========

A finite state machine is a useful computational contraption for
modeling _state_ as it receives _signals_ that cause it to
_transition_ to other states. Their uses are far and broad: embedded
systems, stateful electronic circuits, user interface widgets,
programming language parsing, and so on.

For example, say we have a social robot that looks for faces, and when
it finds one it moves towards their new friend. If the person is still
there when the robot stops, it does a dance. If not, it runs away,
crying.

It has the following states:

* **Scanning**: the robot sits still but uses its camera eyes to look
    for faces.
* **Moving**: the robot is moving towards a face.
* **Staring**: the robot tries to gaze into the face of their friend.
* **Dancing**: the robot is dancing a jig.
* **Running**: the robot is running away.

The same robot can receive _signals_ that cause it to transition from
one state to another:

* **No Face**: robot eye has seen a face.
* **Found Face**: robot eye has seen a face.
* **Done Moving**: robot has moved into position.
* **Friend Ditched Us**: the friend isn't there any more.
* **Friend Still There**: the friend isn't there any more.
* **Dance Over**: robot is done dancing.
* **Run Over**: robot has stopped running.

![](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-10-fsm/robot-fsm-example.png)

There is an _initial state_ indicated with an arrow that doesn't begin
from a state. You can see it entering _Scanning_, which is this FSM's
initial state.

States, Events, Transitions
======

States are nodes in this kind of graph. They represent some status
condition. A state might be used by a graphics system to determine how
to draw some UI widget. Or in a programming language parser, it might
tell us if what it has seen is syntactically correct.

Events are the edges in this kind of graph. They represent signals,
and may come from the world (e.g. a face appearing in front of the
robot's camera), or they may come from something we control (e.g. a
timer saying we're done running away).

When we receive an event, we may or may not _transition_ into some
other state. For example, if the robot is running away but happens to
see a face, it will ignore that event, because the only event that
causes us to transition from the "running" state is "done moving".

If we are in the "staring" state, we have two possible events that
will cause a transition. Either "friend ditched us", which causes a
transition to "running", or "friend still there", which sends us to
"dancing".

Notice that we can have transitions that start and end on the same
node. This can be useful due to transition actions.

Some FSMs (called _Deterministic Finite Automata_, or _DFA_) have
special states that are declared 'accepting' states. When these states
are active, we know that the sequence of input that brought us there
is in some way correct. These are most commonly used in parsing
regular languages. 

Often, an accepting state is drawn with a double-circle, like in the
drawing below.

Error Transitions
------

If we are in a state and we expect to receive events 'foo' or 'bar',
we might want to have a special transition that we take in the event
that we receive _anything else_. These are "failure" transitions that
put us to a known location if the input is not what we expect, or what
we are looking for.

Say we have a DFA that will tell us if an input string spells
'BIN'. It looks like this:

![](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-10-fsm/fsm-bin.png)

This includes positively defined events. For example, if we are in the
'B' state and we receive an 'I' event, we transition to the 'I'
state. But it also includes error transitions, where if we get
anything other than what we're looking for, we transition to a special
failure node (from which we can't escape).

:(

We will use these error transitions in the assignment.

Actions
========

(Actions are not used in this HW assignment)

When a FSM receives a signal that triggers a transition, we may
perform actions. These actions may be associated with entering or
exiting the _state_ (regardless of which signal caused the
transition). Other actions may be associated with following a
_transition_.

Typically the action order is important. When transitioning from
states S1 to S2 along transition edge T, actions are performed in this
sequence:

* S1's exit action
* T's action
* S2's entry action

The actions associated with each state do not depend on which
transition brought us there.


