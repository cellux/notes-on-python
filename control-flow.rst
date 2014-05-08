Control flow
============

if
--

::

    def letterGrade(score):
        if score >= 90:
            letter = 'A'
        elif score >= 80:
            letter = 'B'
        elif score >= 70:
            letter = 'C'
        elif score >= 60:
            letter = 'D'
        else:
            letter = 'F'
        return letter

while
-----

::

    import tempfile, contextlib, urllib2

    def download(url):
        """Download a file from `url` and write it into a temporary file.
    
        Return a file-like object `tmp` for the temp file, which will be
        automatically removed when closed (or when the program
        terminates).
    
        The pathname of the temporary file can be found in `tmp.name`.
        """
        tmp = tempfile.NamedTemporaryFile(prefix='build.py-download.')
        with logger("Downloading {0} to {1}", url, tmp.name):
            with contextlib.closing(urllib2.urlopen(url)) as f:
                while True:
                    buf = f.read(4096)
                    if not buf:
                        break
                    tmp.write(buf)
        return tmp

The ``break`` statement can be used to exit the loop. It causes execution to continue with the the first statement following the loop.

for
---

The ``for`` statement is used to iterate over the elements of a sequence (such as a string, tuple or list) or other iterable object::

    def parse_qsl(qs, keep_blank_values=0, strict_parsing=0):
        """Parse a query given as a string argument.
    
        Arguments:
    
        qs: percent-encoded query string to be parsed
    
        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.  A
            true value indicates that blanks should be retained as blank
            strings.  The default false value indicates that blank values
            are to be ignored and treated as if they were  not included.
    
        strict_parsing: flag indicating what to do with parsing errors. If
            false (the default), errors are silently ignored. If true,
            errors raise a ValueError exception.
    
        Returns a list, as G-d intended.
        """
        pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
        r = []
        for name_value in pairs:
            if not name_value and not strict_parsing:
                continue
            nv = name_value.split('=', 1)
            if len(nv) != 2:
                if strict_parsing:
                    raise ValueError, "bad query field: %r" % (name_value,)
                # Handle case of a control-name with no equal sign
                if keep_blank_values:
                    nv.append('')
                else:
                    continue
            if len(nv[1]) or keep_blank_values:
                name = unquote(nv[0].replace('+', ' '))
                value = unquote(nv[1].replace('+', ' '))
                r.append((name, value))
    
        return r

The ``continue`` statement can be used to continue with the next iteration of the loop.

Range
#####

The built-in function ``range()`` returns a sequence of integers suitable for emulation of the standard integer-indexed loop::

    always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   'abcdefghijklmnopqrstuvwxyz'
                   '0123456789' '_.-')
    safe_map = {}
    for i, c in zip(range(256), str(bytearray(range(256)))):
        safe_map[c] = c if (i < 128 and c in always_safe) else '%{:02X}'.format(i)

To ease understanding of the previous example::

  >>> range(8)
  [0, 1, 2, 3, 4, 5, 6, 7]
  >>> str(bytearray(range(8)))
  '\x00\x01\x02\x03\x04\x05\x06\x07'
  >>> zip(range(8), str(bytearray(range(8))))
  [(0, '\x00'), (1, '\x01'), (2, '\x02'), (3, '\x03'), (4, '\x04'), (5, '\x05'), (6, '\x06'), (7, '\x07')]
  >>> '%{:02X}'.format(65)
  '%41'

Help on built-in function ``range`` in module ``__builtin__``:

    range(...)
        range([start,] stop[, step]) -> list of integers
        
        Return a list containing an arithmetic progression of integers.
        range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0.
        When step is given, it specifies the increment (or decrement).
        For example, range(4) returns [0, 1, 2, 3].  The end point is omitted!
        These are exactly the valid indices for a list of 4 elements.

Else clause on for/while loops
##############################

Both ``for`` and ``while`` loops may be extended with an optional ``else`` clause which is executed if the loop exited cleanly (= not through a ``break`` statement)::

    for value in values:
        if value == 5:
            print "Found it!"
            break
    else:
        print "Nowhere to be found. :-("

Another example::

    while value < threshold:
        if not process_acceptable_value(value):
            # something went wrong, exit the loop; don't pass go, don't collect 200
            break
        value = update(value)
    else:
        # value >= threshold; pass go, collect 200
        handle_threshold_reached()
