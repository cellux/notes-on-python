Operators
=========

Math
----

neg
###

   >>> -5
   -5

pos
###

   >>> +5
   5

add
###

   >>> 5 + 2
   7

sub
###

   >>> 5 - 2
   3

mul
###

   >>> 5 * 2
   10

truediv
#######

   >>> 5 / 2
   2
   >>> 5.0 / 2
   2.5

.. note::

   In Python 3, truediv (``/``) always results in a floating point value:

   >>> 5 / 2
   2.5

floordiv
########

   >>> 5 // 2
   2

pow
###

   >>> 5 ** 2
   25

mod
###

   >>> 5 % 2
   1

Bitwise
-------

lshift
######

   >>> 5 << 2
   20

rshift
######

   >>> 5 >> 2
   1
   >>> 7 >> 2
   1
   >>> 8 >> 2
   2

and
###

   >>> 5 & 2
   0

or
##

   >>> 5 | 2
   7

xor
###

   >>> 5 ^ 2
   7
   >>> 5 ^ 2 ^ 2
   5

invert
######

   >>> ~5
   -6

Comparison
----------

lt
##

   >>> 5 < 2
   False

le
##

   >>> 5 <= 2
   False

eq
##

   >>> 5 == 2
   False

ne
##

   >>> 5 != 2
   True
   >>> 5 <> 2 # same as !=, Python 2 only, deprecated
   True

ge
##

   >>> 5 >= 2
   True

gt
##

   >>> 5 > 2
   True

Boolean
-------

and
###

   >>> 5 > 2 and 2 < 5
   True

``and`` returns the first of its operands (from left to right) whose truth value is False (= the first ``x`` in the list of operands for which ``bool(x)`` returns ``False``)::

   >>> [] and "that"
   []

If all operands are logically true, ``and`` returns the last one::

   >>> "this" and "that"
   'that'

or
##

   >>> 5 > 2 or 2 < 5
   True

``or`` returns the first of its operands whose truth value is True::

   >>> [] or "that"
   'that'

If all operands are logically false, ``or`` returns the last one::

   >>> "" or () or {}
   {}

.. note:: Both ``and`` and ``or`` have short-circuiting behavior.

not
###

   >>> not 5 > 2
   False

Length
------

len
###

   >>> len("abc")
   3
   >>> len([])
   0
   >>> len({1,2,3})
   3
   >>> len({'a':5,'b':3})
   2

Concatenation
-------------

concat
######

   >>> "abc" + "def"
   'abcdef'
   >>> [1,2,3] + [4,5]
   [1, 2, 3, 4, 5]
   >>> (1,2,3) + (4,5)
   (1, 2, 3, 4, 5)
   >>> {'a':5} + {'b':3}
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: unsupported operand type(s) for +: 'dict' and 'dict'

Membership test
---------------

contains
########

   >>> "a" in "snake"
   True
   >>> 5 in [1,2,3]
   False
   >>> 5 in (4,5,6)
   True
   >>> 'a' in {'a':1,'b':3,'c':5}
   True
   >>> 1 in {'a':1,'b':3,'c':5}
   False

Identity test
-------------

is
##

   >>> 5 is 5
   True
   >>> 5 is 3
   False
   >>> "abc" is "abc"
   True
   >>> a = "abc"
   >>> b = "ab" + "c"
   >>> a is b
   True
   >>> 5 is 3+2
   True

is not
######

   >>> 5 is not 5
   False
   >>> 5 is not 3
   True

Indexing
--------

setitem
#######

   >>> a = [1,2,3]
   >>> a[1] = 5
   >>> a
   [1, 5, 3]
   >>> a[-1] = 8
   >>> a
   [1, 5, 8]

   >>> h = {'a':1,'b':3,'c':5}
   >>> h['a'] = 11
   >>> h
   {'a': 11, 'c': 5, 'b': 3}

delitem
#######

   >>> a = [1,5,8]
   >>> del a[1]
   >>> a
   [1, 8]

   >>> h = {'a': 11, 'c': 5, 'b': 3}
   >>> del h['b']
   >>> h
   {'a': 11, 'c': 5}

getitem
#######

   >>> a = [1,5,8]
   >>> a[0]
   1
   >>> a[3]
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   IndexError: list index out of range

   >>> h = {'a': 11, 'c': 5, 'b': 3}
   >>> h['c']
   5
   >>> h['d']
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   KeyError: 'd'

Slicing
-------

    >>> a = [1,2,3]
    >>> a[0:2]
    [1, 2]
    >>> a[0:2] = [9]
    >>> a
    [9, 3]

    >>> a = [1,2,3]
    >>> a[-2:]
    [2, 3]
    >>> a[-2:] = [5]
    >>> a
    [1, 5]

    >>> a = [1,2,3]
    >>> id(a)
    140161649245072
    >>> a = [5,6]
    >>> id(a)
    140161649909344

    >>> a=[1,2,3]
    >>> id(a)
    140161649909344
    >>> a[:] = [5,6]
    >>> a
    [5, 6]
    >>> id(a)
    140161649909344

    >>> a = [1,2,3]
    >>> del a[:2]
    >>> a
    [3]

Truth values
------------

   >>> bool(None)
   False
   >>> bool(0)
   False
   >>> bool(1)
   True
   >>> bool(0.0)
   False
   >>> bool(0.1)
   True
   >>> bool(0.00000000000000000000000000000000000000000000000000000000000000000000000000000001)
   True
   >>> bool("")
   False
   >>> bool("abc")
   True
   >>> bool([])
   False
   >>> bool([1])
   True
   >>> bool({})
   False
   >>> bool({'a':5})
   True
   >>> bool(())
   False
   >>> bool((1,2))
   True
   >>> bool((0))
   False
   >>> bool((0,))
   True

Inplace operators
-----------------

Inplace operators are ``+=``, ``-=``, ``*=``, ``/=``, ``//=``, ``%=``, ``**=``, ``&=``, ``|=``, ``^=``, ``<<=`` and ``>>=``.

    >>> a = 5
    >>> a += 3
    >>> a
    8
    >>> a -= 2
    >>> a
    6
    >>> a *= 3
    >>> a
    18
    >>> a /= 2
    >>> a
    9
