Lexical structure
=================

Indentation
-----------

The block structure of a Python program is determined by the indentation of its code::

    def parse_size(size_string):
        """Parse `size_string` and return the corresponding size in bytes.
    
        The following suffixes may be used in `size_string`: k,K,m,M,g,G
        """
        m = re.match(r'(\d+)([kKmMgG])?$', size_string)
        if not m:
            die("Cannot parse size value: {0}", size_string)
        size = int(m.group(1))
        if m.group(2):
            multipliers = { 'k': 1024, 'm': 1024**2, 'g': 1024**3 }
            size = size * multipliers[m.group(2).lower()]
        return size

    assert parse_size("10k") == 10240

Here we define a function called ``parse_size()`` and then test it with an ``assert`` statement.

Python knows that the ``assert`` does not belong to the function body because it is indented to the same level as the ``def`` statement.

.. tip:: Use four spaces per indent level. Do not use tabs.

Encoding of source files
------------------------

By default, Python 2 uses the 7-bit ASCII character set for program text. (Python 3 uses UTF-8.)

If you want to be explicit about the encoding of your source, use an *encoding declaration* in the first or second line of the file::

  #!/usr/bin/env python
  # -*- coding: utf-8 -*-

  ...

.. note::
   The actual regular expression it tries to match is ``coding[=:]\s*([-\w.]+)``, which means Vim and Emacs modelines both work.

Line endings
------------

All three commonly used end-of-line sequences are recognized:

* ``\n`` (Unix),
* ``\r`` (old Mac),
* ``\r\n`` (Windows).

Comments
--------

Comments are introduced by a ``#`` (hash) character and extend to the end of line.

If you want to comment out several lines, place a ``#`` before each line (preferably preserving the indentation level).

Explicit line joining
---------------------

::

    if 1900 < year < 2100 and 1 <= month <= 12 \
        and 1 <= day <= 31 and 0 <= hour < 24 \
        and 0 <= minute < 60 and 0 <= second < 60:   # Looks like a valid date
             return 1

The backslash-newline sequences are removed by the parser, so the three lines above are seen as if they had been typed on a single line.

Implicit line joining
---------------------

Expressions in parentheses, square brackets or curly braces can be split over more than one line without using backslashes. For example::

    month_names = ['Januari', 'Februari', 'Maart',      # These are the
                   'April',   'Mei',      'Juni',       # Dutch names
                   'Juli',    'Augustus', 'September',  # for the months
                   'Oktober', 'November', 'December']   # of the year

Implicitly continued lines can carry comments.

The indentation of the continuation lines is not important.
