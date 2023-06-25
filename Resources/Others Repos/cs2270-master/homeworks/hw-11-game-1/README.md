Game 
==========

Everybody loves games! Except for people who don't.

This assignment is about using what you've learned about Data
Structures and Algorithms to create a simple game. _This is primarily
a design exercise._ 

Past assignments could test your ability to perform things for which
there was a _right answer_. However most interesting professional
activities after college center on things for which there _is no right
answer_. This assignment is one of those "ill-defined" problems.

Pick or Invent a Game
---------

Think about a game you've played: checkers, chess, poker, StarCraft,
Zork, _or whatever_. Imagine what data structures you might use to
model that game. For example in checkers, you might have a grid data
structure that represents the game world, with data representing what
is in each cell. You'd also need to model what are valid moves, and
create an algorithm that allows the game to unfold in a predictable
sequence (e.g. player 1 moves, then player 2, and so on).

You may re-use an existing game, or invent your own. The important
thing is that you can enumerate the rules in a way that you can
model. And (unless you know something I don't) you will need to model
this using data structures. And the sequence of events that players
take (and how the program reacts) will be determined by some
algorithm.

Groups
--------

This is a group project. Mostly because I will personally look at all
of these, and I can't read and understand 160 of them in a meaningful
way. So: find a group of 3, 4, or 5 people and do the work
together. You'll turn things in individually (see below). 

Come up with a group name. This can be whatever you want.

What To Do
--------

Your game can be text-based or graphical. Remember to not bite off
more than you can chew. _This is partially an exercise in
self-restraint._

Other guidelines:

* Your game should involve at least one player.

* Your game must involve making decisions that modify the game state.

* It must be possible to distinguish between _valid_ and _invalid_
  moves. (E.g. in chess a rook can move horizontally but not
  diagonally).
  
* It must be possible to win _and_ lose.

What To Turn In
----------

You'll turn this in **via email** to me. Please send it to my gmail 
account: `gabe.johnson@gmail.com` and use the subject 
line `CS 2270 Project`.

Retrograde is not involved in this assignment.

Send a tarball or zip file that has the following directory
structure, where `CoolGroupName` is the name of your group. I will
unpack your archive in a directory with everybody else so it is
important that it be in a directory.

	CoolGroupName/
		group.txt
		introspection.txt
		code/
			(all your code here)
			
The `group.txt` file lists all the group members including student ID.

The `introspection.txt` file is the really important thing.  


**The introspection file must be less than 500 words.** You can use
  the `wc` Unix/Linux command to see how big a text file is. This
  works from the terminal on Macs as well:
  
	  wc -w introspection.txt

Sections for the introspection.txt file:

1. Initial ideas: enumerate the list of crazy and not-so-crazy ideas
that you initially had for your game.

2. Pivots: list the spots where you changed your mind because you
wanted to make something easier (or harder) on your team. Explain why.

3. Data structures: What data structures did you use? Why did you
choose them? What alternate structures would be appropriate? Why
didn’t you choose those?

4. Describe the hardest aspect of this assignment.

Next Week
-------

The assignment after this one will be an extra credit assignment to
create an A.I. player for your game. Keep that in mind as you work on
this week's assignment, if you plan on doing the A.I.
