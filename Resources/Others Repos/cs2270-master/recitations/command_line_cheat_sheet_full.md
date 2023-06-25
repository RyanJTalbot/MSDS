Linux Commands
========

This was originally put together by Andrew Sayler. If you want a
shorter list of only the common commands with more instructions, see
the other version of this file (in the same directory).

Getting Help
------
- man - The Unix/Linux Manual
- info - Supplemental Manual (Mainly for GNU Software)
- <cmd> -h | --help | --usage | -help | ...

Files and Directories
-------
- pwd - Print Working Directory
- cd - Change Directory
- ls - List Files
- stat - Get Detailed File Info
- touch - Create New Empty File
- cp - Copy
- mv - Move/Rename
- rm - Remove/Delete
- mkdir - Make new directory
- rmdir - Remove empty directory
- chmod - Change File/Directory Permissions
- chown - Change File/Directory Owner
- find - Find files and directories and act on them
- locate - Find files and directories using an indexed search
- tar - Archive/compress or unarchive/decompress a file or directory (.tar, .xz, etc)
- zip - zip a file or directory
- unzip - unzip a file or directory

File Contents
--------
- cat - Print file to standard output
- grep - Match file contents using regular expressions
- sed - Transform file contents using regular expressions
- awk - sed’s best friend
- md5sum - Verify file contents (also sha*sum)
- sort - Sort file contents
- uniq - Count duplicate lines
- cut - Isolate fields in a file
- more - The original file ‘pager’
- less - An updated ‘more’
- head - Print first N lines of a file
- tail - Print last N lines of a file
- tee - Split standard input between a file and the terminal

Remote Access
--------
- ssh - Securely log into remote server
- scp/sftp - Transfer files over ssh
- rsync - Perform a differential transfer of files locally or via SSH
- ssh-keygen - Generate local RSA key for use with passwordless SSH access
- ssh-copy-id - Upload RSA public key to remote server for passwordless SSH access
- sshfs - Mount a remote directory to the local file system via SSH
- screen - A terminal multiplexer
- tmux - Another terminal multiplexer

Packages
----------
- apt-get - Upgrade, add, and remove Debian/Ubuntu Packages
- apt-cache - List and Search for Available Packages

System
-------
- exit - Close Terminal
- sudo - Run as Superuser (root)
- su - Login as Superuser (root), or sudo -i
- kill/pkill - Send signals to processes
- poweroff - Shutdown system
- shutdown - Shutdown or restart system

Diagnostics
--------
- ps - List running processes
- top - Interactive ps
- lspci - List hardware devices
- lsusb - List usb devices
- lsblk - List block devices
- findmnt - List mountpoints
- netstat - List open ports and sockets
- ip - List network interface information
- ifconfig - List network interface information (deprecated in favor of IP)
- sensors - List readings from thermal and other sensors
- lsmod - List loaded kernel modules
- w/who/users - List logged in users and what they are doing
- uptime - See how long computer has been running
- time - Get info on program execution

Build Tools
--------
- make - Auto-generate files from predefined recipes
- gcc - The GNU Compiler Collection (C/, C++, ObjC, Java, Ada, Go, Fortran)
- autoconf - Automatically generate configure scripts
- automake - Automatically generate Makefiles
- gdb - The GNU debugger
- valgrind - Analyze memory usage and execution profile
