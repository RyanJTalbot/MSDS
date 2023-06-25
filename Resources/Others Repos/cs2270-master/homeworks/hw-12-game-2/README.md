Game Scenario: Develop an AI player
===========

This is an **extra credit** assignment worth 15 points. It is based on last week's game.

This is very simple: create an AI player that either:

1) Plays the game in the same way the player does, or
2) Manipulates the game in some way to make it difficult for the player.

The requirements are very loose. As long as you write code that make decisions based on 
the game state, that is acceptable.

Example 1: Pong
-------

If you made a Pong-like game, you might write an AI that controls the other paddle. 
To make it interesting, the AI might have a parameter that controls how effective it
is. On the 'easy' setting it might just move around randomly; 'medium' might move
in the general direction of the ball but not be able to control the speed; 'hard' 
might be able to play a perfect game.

Example 2: Tetris
---------

Since Tetris is basically a single-player game, the AI here could be the code that
determines which pieces to give you. This might work against you (always giving you the 
worst possible piece), or with you (it hooks you up with the best pieces). It might
be tempermental: the better you do, the more it works against you. Or the worse you do, 
the more it helps.

What to Turn In
======

Similar to last week, but the subject line will be different.

Send an archive (see below) to my gmail account: `gabe.johnson@gmail.com`.

Subject line: `CS 2270 AI`

**Archive:** Similar to last week. Make an archive called `OurGroup.zip` (or a 
tarball, or whatever) that _unpacks into to some directory that is named
after your group_. Include code, the group file, and introspection file. 
Like this:

    OurGroup/
        code/
            < all your code here>
        group.txt
        introspection.txt
