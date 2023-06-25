Binary Trees (C++ specific notes)
===========

This week the homework is on binary search trees. I created a
comprehensive driver so you can try your code on your local machine
before uploading it to RetroGrade. Don't get too used to this, though:
it is absolutely necessary that you be able to write your own test
code. And to write your own test code, you need to be able to ask
questions like "what happens if I do something crazy here? What if I
try to remove a node that isn't in the tree? Or if it is a tree
composed only of a million zeros? Will that still work?"

Git Instructions
--------

You should use git. This isn't required, but it will make life easier
for you. _Note: in the below examples I am putting the code just off
your home directory. If you are using Dropbox, replace the `~` symbol
with `~/Dropbox`._

If you have __not yet cloned the github repository__ you only need to
do this one time:

	cd ~
    git clone https://github.com/johnsogg/cs2270.git

If you __already cloned the github repository__ you can cd into your
repository and `pull` any changes (including lecture slides, all the
homework files, etc.):

    cd ~/cs2270
	git pull

Now that you have a copy of the repository you may cd into the binary
trees homework directory to build and run the driver.

	cd ~/cs2270/homeworks/hw-2-binary-search-trees/cpp
	make
	./binary_search_tree_driver
	
It will compile with warnings complaining about unused
parameters. This is because you haven't implemented anything yet. When
you run the driver, it will not get very far before it segfaults. 

(By the way, why does it do this? I can 100% guarantee that on the
first test I will ask about segfaults, what they mean, how you can
track them down, how you fix them.)

Email Policy
---------

For the last homework, I spent probably about 25 hours responding to
student email. It is _fantastic_ that you are willing to ask
questions. Keep doing that! _But_, many of the emails indicated that
people weren't thinking critically, or asking around among their
peers. So for this assignment, I am instituting a policy for sending
me email about this. This does two things. First, it means you have to
start learning how to troubleshoot problems on your own (which is one
of the primary skills of a software engineer), and it means that when
I do get email from a student it is likely something really weird, and
I enjoy troubleshooting weird things.

Please read the new email policy, which can be found in the top-most
directory in the github repository, in the file `email_policy.md`.

Turning In Your Homework
==========

Upload your `binary_search_tree.cpp` file. Nothing else is needed.
