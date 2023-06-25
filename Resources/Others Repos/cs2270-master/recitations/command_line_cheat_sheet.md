Linux Commands
========

This was originally put together by Andrew Sayler and simplified for
CS 1300 and 2270 by Gabe Johnson.

Getting Help
------
- man - The Unix/Linux Manual. _Also helpful to just Google for
  things._
- <cmd> -h | --help | --usage | -help | ... _Many commands let you use
  a -h or --help flag to get quick help._

Files and Directories
-------
- pwd - Print Working Directory. _Where am I on my disk?_
- cd - Change Directory. _like "cd cs1300"_
- ls - List Files. _like 'ls, or ls ~, or ls some-directory/'_
- cp - Copy. _like 'cp original-file.txt destination-file.txt'_
- mv - Move/Rename. _like 'mv original-file.txt destination-file.txt'_
- rm - Remove/Delete. _like 'rm doomed-file.txt'_
- mkdir - Make new directory. _like 'mkdir my-source-files'_
- rmdir - Remove empty directory. _like 'rmdir my-doomed-directory'_
- chmod - Change File/Directory Permissions. _like 'chmod +x my-program'_

File Contents
--------
- cat - Print file to standard output. _like 'cat my-program.py'_
- less - Display file contents (q to exit)
- grep - Match file contents using regular expressions

System and Diagnostics
-------
- exit - Close Terminal
- sudo - Run as Superuser (root)
- kill/pkill - Send signals to processes
- ps - List running processes
- top - Interactive ps

Build Tools
--------
- make - Auto-generate files from predefined recipes
- gcc - The GNU Compiler Collection (C/, C++, ObjC, Java, Ada, Go, Fortran)
