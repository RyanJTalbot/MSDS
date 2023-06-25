CU's Computing Environment
============

_Note: This is an evolving document. Tips and tricks may (or may not)
be put here._


The department has their own instructions for getting and installing
the VM. You can see them
[here](http://moodle.cs.colorado.edu/course/view.php?id=78).

Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (~100
MB) and install it.

> This software is one example of a Virtual Machine (VM). It is a
  program that provides a simulated computer. In this case, the
  simulation includes with its own processor, memory, disks, and other
  hardware. For a VM like this to be useful you need to supply it with
  a VM Image (see the next item).
  
Download the
[GIGANTIC VM Image](http://moodle.cs.colorado.edu/mod/page/view.php?id=2986)
from the CS department Moodle. The Moodle is a password protected
thing, so you'll need to create an account, then install a BitTorrent
client to get the image. That web page explains all of that.

Alternately, if you want to help kill the department file server, you
can use the
[direct link](http://foundation.cs.colorado.edu/files/CU-CS-VM-S13-v1.1.ova)
or [mirror](http://condor.andysayler.com/files/CU-CS-VM-S13-v1.1.ova).

> This file specifies a fully functional Ubuntu Linux instance. It is
  huge, so when you start downloading this, expect it to take a
  while. We provide this so everybody has a common computing
  environment. Linux is chosen because it is an incredibly powerful,
  programmer-friendly operating system. The Ubuntu flavor is chosen
  because it is relatively user-friendly.
  
Once the VM is installed and the Linux VM Image is downloaded, go
ahead and run the VM. You will see something like this:

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-1.png)

Go to the menu and choose _File_ / _Import Appliance_. Follow the
dialog until you can pick the GIGANTIC VM Image:

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-2.png)

After picking the right file, keep following the dialog, and click
_Import_. It will then load the contents of the image file into its
working format. _This takes a while... on my machine it is long enough
to make coffee._

... coffee ...

Eventually it finishes and you are greeted with this:

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-3.png)

It is 'powered off' by default, and that doesn't help us much. So go
ahead and boot the machine by clicking _Start_.

While booting, several dialogs will pop up with sort of confusing
information about how the mouse and keyboard are captured by the
VM. All this means is that if you want to "get out" of the VM (so you
can use your other applications) you'll have to use the mouse. If you
figure out how to use the keyboard to alt-tab away, let me know so I
can update this document.

At last, your virtual Ubuntu computer has booted. I opened a few
windows to make this screenshot more interesting. You will see
something that looks like this:

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-4.png)

[Click here to see a big version of that desktop screenshot.](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-4-large.png) 

In that screenshot I have written a little C++ program called "Hello
World". You can also see the commands I typed into the terminal on the
left. I compiled my program and ran it---you can see that it wrote
"Hello World! I am alive!" to the console. If you can replicate this,
students in CS 1300 will be a good way towards being done with the
first week's homework assignment.

When you are done using the Ubuntu virtual machine, you can just quit
Virtual Box. It will ask you what you want to do, as illustrated here:

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-5.png)

If you want to be able to keep going where you left off, save the
machine state. If you do this, the next time you load Virtual Box,
your previous session is available in a list. You even get a pleasant
black-and-white image with artistic interlace to give you a hint about
what it looks like.

![](https://raw.github.com/johnsogg/cs1300/master/recitations/img/virt-box-6.png)

We will cover basics of how to use Ubuntu and (more importantly) the
command line interface later on.

Something to think about
--------

Is it possible to run another virtual machine _inside an existing
virtual machine_? What about running a VM inside that double-nested
one? Where does this madness end?

If you Google around for it, you will find some that some people have
turned this into a rather... _interesting_ hobby.
