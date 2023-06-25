UTFramework
==================

Author: *Alec G Thilenius*

Version: *1.2.2*

A simple unit testing framework designed to be bundled with homework assignments. The Framework is also being used as a back end driver for RetroGrade, the online grading system create by Gabe. These files will be updated when a new release has been tested and stabilize.

Important!
-------
If you use a makefile from a previous assignment, or you make your own, you MUST add -pthread to the end of the flags:

CXXFLAGS = -g -Wall -Wextra -Wno-write-strings2 -pthread

Building
-------
To build the demo Main.cpp, simply pull all the files ( Main.cpp, UTFramework.cpp, UTFramework.h, makefile ) and use the provided make file. Give the test a few seconds to run, the infinite loop will be terminated after a few seconds if you are on a Linux machine.

Support
-------

*Supported:*
* Linux
* WIN32 VC++ ( Reduced functionality )
* Infinite loop detection and recovery
* std::exception catching
* unknown exception catching
* Segmentation Fault catching
** Note SegFault catching via POSIX handler. Must be a POSIX compatible system.

*Reduced Functionality:*
* Infinite loop detection is disabled in WINDOWS
* SegFault handling may not work as intended in VS2012

Help
--------

Please contact me if you find a bug or have questions at Alec.Thilenius@Colorado.edu

Lisence
--------

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
