Input & Output
==============

Printing stuff
--------------

The print statement
###################

  >>> print "hello, world\n"
  hello, world

  >>> print 3.14, "abc", (1,2,3)
  3.14 abc (1, 2, 3)

The ``print`` statement evaluates each given expression in turn and writes the string representation of the resulting objects to standard output (``sys.stdout``).

A space is written before each item, unless the output system believes it is positioned at the beginning of a line.

A new-line character is written at the end, unless the print statement ends with a comma::

  >>> print 1,2,3; print 5
  1 2 3
  5
  >>> print 1,2,3,; print 5
  1 2 3 5

You can print to any file-like object using the "chevron" (``>>``) syntax::

  >>> import sys
  >>> print >> sys.stderr, "This is an error message.\n"
  This is an error message.

  >>> print >> open("/etc/motd", "w"), "This is the message for today.\n"
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  IOError: [Errno 13] Permission denied: '/etc/motd'
  >>>

The print function
##################

Python 3 dropped the ``print`` statement, there is only a ``print()`` function which was backported to Python 2 (>= 2.6) as well.

To make the new-style ``print()`` available in Python 2, you must explicitly backport it from the future::

  >>> from __future__ import print_function
  >>> print(1,2,3,sep='-')
  1-2-3
  >>> print(1,2,3,end='\r\n')
  1 2 3
  >>> print(1,2,3,file=sys.stderr)
  1 2 3

If you want to print something without a newline at the end::

  >>> print('something', end='')

The standard streams
--------------------

Every program has access to three pre-defined streams: standard input (``stdin``), standard output (``stdout``) and standard error (``stderr``).

These correspond to file descriptors 0, 1 and 2.

Python wraps these descriptors with three file-like objects defined in the ``sys`` module::

  >>> import sys
  >>> sys.stdin.fileno()
  0
  >>> sys.stdout.fileno()
  1
  >>> sys.stderr.fileno()
  2

You can write something to ``sys.stdout`` and ``sys.stderr`` using the ``write()`` method::

  >>> sys.stdout.write("Hello, world!\n")
  Hello, world!

Flushing
########

If you want to make sure that the written data arrives immediately at the destination (which may be a log file), flush the stream after writing::

  >>> sys.stdout.flush()

If ``sys.stdout`` is a line buffered stream (like a tty), and you want to write something like::

  Doing operation: done.

with some potentially long operation taking place between ``Doing operation:`` and ``done.``, then calling ``flush()`` after printing the first part makes sure it appears immediately on output.

(Making ``sys.stdout`` unbuffered is another option, but that may slow things down.)

Echo server example
###################

::

  #!/usr/bin/env python

  import sys

  while True:
      line = sys.stdin.readline()
      if not line or line.strip() in ('quit','exit','leave','bye'):
          break
      sys.stdout.write(line)

You can connect stdin/stdout to a real network socket using ``socat``::

   socat TCP4-LISTEN:5555,fork,reuseaddr EXEC:./echo.py,pty,echo=0,raw

Files
-----

You can open a file using the ``open()`` built-in function::

  >>> open('/etc/passwd')
  <open file '/etc/passwd', mode 'r' at 0x7fd1028fdf60>

The ``file`` object returned by ``open()`` has lots of handy methods::

  >>> f = open('/etc/passwd')
  >>> f.readline()
  'root:x:0:0:root:/root:/bin/bash\n'
  >>> f.readline()
  'daemon:x:1:1:daemon:/usr/sbin:/bin/sh\n'
  >>> len(f.readlines())
  45
  >>> f.readline()
  ''
  >>> f.seek(0)
  >>> f.tell()
  0
  >>> f.readline()
  'root:x:0:0:root:/root:/bin/bash\n'
  >>> f.tell()
  32
  >>> f.close()

A ``file`` is an iterable object::

    def getpw(uid):
        """Return the line from /etc/passwd belonging to the user with the given uid."""
        with open("/etc/passwd") as f:
            for line in f:
                line = line.strip()
                fields = line.split(':')
                if int(fields[2]) != uid:
                    continue
                return line

::

    >>> getpw(0)
    'root:x:0:0:root:/root:/bin/bash'

Choosing the right open mode
############################

Files are opened in read-only mode by default. You can override this by passing a second ``mode`` argument to ``open()``:

  >>> f = open("myfile.txt", "w") # write-only
  >>> f.write("this is a line\n")
  >>> f.seek(0)
  >>> f.readline()
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  IOError: File not open for reading
  >>> f.close()

Possible values for the ``mode`` argument:

============= =========== =================
Mode argument Meaning     Truncates file?  
============= =========== =================
``'r'``       read-only   no               
``'r+'``      read/write  no               
``'w'``       write-only  yes              
``'w+'``      read/write  yes              
``'a'``       append-only no               
``'a+'``      append/read no               
============= =========== =================

Passing ``"w"`` or ``"w+"`` as the mode clobbers the existing contents of the file. If you don't want this to happen, use ``"r+"`` (read/write), ``"a"`` (append) or ``"a+"`` (append/read) as the mode.

Binary mode
###########

On Windows, ``'b'`` appended to the mode opens the file in *binary mode*, so there are also modes like ``'rb'``, ``'wb'``, and ``'r+b'``. Python on Windows makes a distinction between text and binary files; the end-of-line characters in text files are automatically altered slightly when data is read or written. This behind-the-scenes modification to file data is fine for ASCII text files, but it’ll corrupt binary data like that in JPEG or EXE files. Be very careful to use binary mode when reading and writing such files. On Unix, it doesn’t hurt to append a ``'b'`` to the mode, so you can use it platform-independently for all binary files.

A simple cross-platform file copier::

    BLOCK_SIZE = 4096

    def copy_file(src, dst):
        with open(src, "rb") as srcf:
            with open(dst, "wb") as dstf:
                while True:
                    buf = srcf.read(BLOCK_SIZE)
                    if not buf:
                        break
                    dstf.write(buf)

Universal newline support
#########################

Add a ``'U'`` to mode to open the file for input with *universal newline support*.

Any line ending in the input file will be seen as a ``'\n'`` in Python.

Also, a file so opened gains the attribute ``'newlines'``; the value for this attribute is one of ``None`` (no newline read yet), ``'\r'``, ``'\n'``, ``'\r\n'`` or a tuple containing all the newline types seen::

  >>> f = open("myfile.txt", "wb")
  >>> f.write("first\r")
  >>> f.write("second\r")
  >>> f.close()
  >>> f = open("myfile.txt")
  >>> f.readline()
  'first\rsecond\r'
  >>> f.close()
  >>> f = open("myfile.txt", "U")
  >>> f.readline()
  'first\n'
  >>> f.newlines
  >>> f.readline()
  'second\n'
  >>> f.newlines
  '\r'
  >>> f.close()
