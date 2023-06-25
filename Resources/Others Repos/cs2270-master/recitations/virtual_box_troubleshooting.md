Virtual Box Troubleshooting
===========

_(This is modified from an email from Andrew Sayler.)_

Many problems with Virtual Box are almost always the result of one of
the following:

1. A bad download of the VM file. This can be checked by comparing the
published checksum (MD5) to the checksum of the download as discussed
on the
[CS Moodle](http://moodle.cs.colorado.edu/mod/page/view.php?id=2986).

1. The student changing the VM configuration from the default
values. I believe this is what happened in one student's case since it
appears that she somehow enabled UEFI booting for the VM instead of
the default legacy BOIS booting that the VM is configured to support.

1. I'd also encourage you to encourage your students to use Dropbox on
the VM to store their work files. The VM does tend to be more prone to
file system corruption (since it is a FS atop a FS and can run into
issues with ungraceful shutdowns, etc) then a standard computer. By
storing their files in Dropbox, the students can ensure that these
files will not be lost if they are forced to re-install their VM at
some point. Dropbox is already installed and setup on the VM, the
student must just log in and start using it to store their
files. Further directions are available on the VM Moodle site.
