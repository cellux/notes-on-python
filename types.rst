Standard types
==============

Numbers
-------

Integers
########

    >>> 123
    123
    >>> 0o755
    493
    >>> 0x1000
    4096
    >>> 0b1001
    9

A string (or another number) can be converted to an integer with the ``int()`` constructor::

    >>> int("1234")
    1234
    >>> int(3.25)
    3
    >>> int(-3.25)
    -3

If the string representation is not in base 10, pass the desired base as the second argument::

    >>> int("0x1000")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: invalid literal for int() with base 10: '0x1000'
    >>> int("0x1000", 16)
    4096

The radix prefix is optional::

    >>> int("1000", 16)
    4096
    >>> int("1001", 2)
    9

Integer values which do not fit into a processor register are automatically and transparently converted into *long integers* which have unlimited range, subject to available (virtual) memory only::

    >>> int(100000000000000000000000000000000000000000000000000000)
    100000000000000000000000000000000000000000000000000000L
    >>> type(100000000000000000000000000000000000000000000000000000L)
    <type 'long'>

Floats
######

    >>> 3.14
    3.14
    >>> 10.
    10.0
    >>> .001
    0.001
    >>> 1e100
    1e+100
    >>> 3.14e-10
    3.14e-10
    >>> 0e0
    0.0

A string (or a number) can be converted to floating point with the ``float()`` constructor::

  >>> float(3)
  3.0
  >>> float("3.5")
  3.5

Floats are stored as C doubles and are subject to the usual floating point inaccuracies::

  >>> float("1234.1252352375923759823759823759235923628305682309682049682490683490683")
  1234.1252352375923
  >>> 1.021-0.021
  0.9999999999999999

Strings
-------

String literals
###############

String literals can be enclosed in matching single (``'``) or double (``"``) quotes::

    >>> 'a string in single quotes'
    'a string in single quotes'
    >>> "a string in double quotes"
    'a string in double quotes'

There is no difference between the interpretation of the two variants.

The string delimiter (``'`` or ``"``) – if it occurs in the string - must be escaped with a backslash::

    >>> 'I\'m not hungry.'
    "I'm not hungry."
    >>> "\"What do you think?\" - he asked."
    '"What do you think?" - he asked.'

.. tip:: Use ``'...'`` for strings which are used as enums or constants (values chosen from a known, finite set) and ``"..."`` for arbitrary strings.

The following escape sequences are interpreted in strings:

=============== ==================================
Escape sequence Meaning
=============== ==================================
``\a``          BEL (Bell)
``\b``          BS (Backspace)
``\f``          FF (Form Feed)
``\n``          NL (New Line)
``\r``          CR (Carriage Return)
``\t``          TAB (Horizontal Tab)
``\v``          VT (Vertical Tab)
``\\``          backslash
``\'``          single quote
``\"``          double quote
``\xhh``        character with hex value ``hh``
``\ooo``        character with octal value ``ooo``
=============== ==================================

::

     >>> "ab\x63d"
     'abcd'
     >>> "ab\x0d\x0acd"
     'ab\r\ncd'

Byte vs. character semantics
############################

In Python 2, there are two different string types: ``str`` holds a sequence of bytes, while ``unicode`` holds a sequence of characters (Unicode code points).

When the parser encounters a literal string, it packages up the bytes between the quotes as an ``str`` object.

If you want a ``unicode`` object instead, you must use a *Unicode literal*, denoted by a ``u`` or ``U`` prefix::

    >>> u'Árvíztűrő tükörfúrógép'
    u'\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p'

The bytes of program text inside the  ``u'...'`` are interpreted according to the encoding of the source file (defaults: ``ascii`` in Python 2, ``utf-8`` in Python 3).

.. note::
   In Python 3, the ``unicode`` type has gone, ``str`` objects became Unicode strings and there is a new ``bytes`` type for byte strings with its associated ``b'...'`` literal syntax.

The following escape sequences are only interpreted in Unicode literals:

=============== ============================================
Escape sequence Meaning
=============== ============================================
``\N{name}``    Character named name in the Unicode database
``\uxxxx``      Character with 16-bit hex value ``xxxx``
``\Uxxxxxxxx``  Character with 32-bit hex value ``xxxxxxxx``
=============== ============================================

>>> "ab\u0151"
'ab\\u0151'
>>> u"ab\u0151"
u'ab\u0151'
>>> u"abő"
u'ab\u0151'

Converting from ``unicode`` to ``str``::

    >>> u'Árvíztűrő tükörfúrógép'.encode('latin2')
    '\xc1rv\xedzt\xfbr\xf5 t\xfck\xf6rf\xfar\xf3g\xe9p'
    >>> u'Árvíztűrő tükörfúrógép'.encode('utf-8')
    '\xc3\x81rv\xc3\xadzt\xc5\xb1r\xc5\x91 t\xc3\xbck\xc3\xb6rf\xc3\xbar\xc3\xb3g\xc3\xa9p'
    >>> u'Árvíztűrő tükörfúrógép'.encode('latin1')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    UnicodeEncodeError: 'latin-1' codec can't encode character u'\u0171' in position 6: ordinal not in range(256)

Converting from ``str`` to ``unicode``::

    >>> '\xc1rv\xedzt\xfbr\xf5 t\xfck\xf6rf\xfar\xf3g\xe9p'.decode('latin2')
    u'\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p'
    >>> '\xc3\x81rv\xc3\xadzt\xc5\xb1r\xc5\x91 t\xc3\xbck\xc3\xb6rf\xc3\xbar\xc3\xb3g\xc3\xa9p'.decode('utf-8')
    u'\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p'

Raw string literals
###################

When a string literal is prefixed by ``r`` or ``R``, the backslashes in the string cease to be escapes:

    >>> r'hey\njoe'
    'hey\\njoe'

This comes handy when writing regular expressions:

    >>> r'^(\d\d\d\d)-(\d\d)-(\d\d)$'
    '^(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)$'
    >>> r'(\w+)\.(jpg|png|gif)'
    '(\\w+)\\.(jpg|png|gif)'

.. note:: Raw strings are not a different type, the ``r'...'`` notation is just a parse-time convenience.

Triple-quoted strings
#####################

In triple-quoted strings, unescaped newlines and quotes are allowed (and retained), except that three unescaped quotes in a row terminate the string::

    >>> """This is a long string
    ... which 'is' "continued"
    ... over several lines."""
    'This is a long string\nwhich \'is\' "continued"\nover several lines.'

String literal concatenation
############################

Writing two string literals side by side (with whitespace between them) results in their concatenation *at compile time*, like in C:

    >>> s = "abc" "def"
    >>> s
    'abcdef'

*At run time*, strings can be concatenated with the + operator.

    >>> "abc"+"def"
    'abcdef'

Dealing with characters
#######################

There is no character type, so characters must be represented as string objects with length 1.

    >>> ord('a')
    97
    >>> chr(0x61)
    'a'
    >>> ord(u"ő")
    337
    >>> chr(337)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: chr() arg not in range(256)
    >>> unichr(337)
    u'\u0151'

Commonly used string methods
############################

    >>> "hello".capitalize()
    'Hello'
    >>> "hello".upper()
    'HELLO'
    >>> "hello".upper().lower()
    'hello'

    >>> "hello".center(10)
    '  hello   '

    >>> "hello".startswith('h')
    True
    >>> "hello".endswith('lo')
    True

    >>> "hello".find('ll')
    2
    >>> "hello".find('lll')
    -1
    >>> "hello".index('ll')
    2
    >>> "hello".index('lll')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: substring not found

    >>> "hello".replace('l','L')
    'heLLo'

    >>> "hello".lstrip('h')
    'ello'
    >>> "hello".rstrip('o')
    'hell'
    >>> "hello".rstrip('o').rstrip('l')
    'he'
    >>> "hello".strip('h')
    'ello'
    >>> "\t\t   hello  \t  \n\r\n\r".strip()
    'hello'

    >>> "hello".join("123")
    '1hello2hello3'
    >>> '-'.join([4,5,6])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: sequence item 0: expected string, int found
    >>> '-'.join(['4','5','6'])
    '4-5-6'
    >>> '-'.join('456')
    '4-5-6'

    >>> "hello".split('l')
    ['he', '', 'o']
    >>> '4-5-6'.split('-')
    ['4', '5', '6']

Tuples
------

Tuples are immutable containers holding a sequence of arbitrary Python objects.

Tuples of two or more items are formed by comma-separated lists of expressions (usually written within parentheses, but that's not required)::

    >>> a = 1,2,3
    >>> a
    (1, 2, 3)
    >>> type(a)
    <type 'tuple'>
    >>> a[0]
    1
    >>> a[1]
    2
    >>> a[2]
    3
    >>> a[3]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: tuple index out of range

A tuple of one item (a *singleton*) can be formed by affixing a comma to an expression.

An expression by itself does not create a tuple, since parentheses must be usable for grouping of expressions::

    >>> a = (1)
    >>> a
    1
    >>> type(a)
    <type 'int'>
    >>> a = (1,)
    >>> a
    (1,)
    >>> type(a)
    <type 'tuple'>

An empty tuple can be formed by an empty pair of parentheses:

    >>> a = ()
    >>> type(a)
    <type 'tuple'>

Lists
-----

Lists are mutable containers holding a sequence of arbitrary Python objects.

Lists are formed by placing a comma-separated list of expressions in square brackets::

    >>> l = [1,2,3]
    >>> l
    [1, 2, 3]
    >>> empty_list = []
    >>> list_with_one_element = ['abc']

Note that there are no special cases needed to form lists of length 0 or 1.

Some commonly used list methods
###############################

    >>> l = [1,2,3]
    >>> l.append(4)
    >>> l
    [1, 2, 3, 4]
    >>> l.extend([4,5])
    >>> l
    [1, 2, 3, 4, 4, 5]
    >>> l.index(4)
    3
    >>> l.insert(1,'abc')
    >>> l
    [1, 'abc', 2, 3, 4, 4, 5]
    >>> l.pop()
    5
    >>> l
    [1, 'abc', 2, 3, 4, 4]
    >>> l.pop(0)
    1
    >>> l
    ['abc', 2, 3, 4, 4]
    >>> l.remove(4)
    >>> l
    ['abc', 2, 3, 4]
    >>> l.remove(4)
    >>> l
    ['abc', 2, 3]
    >>> l.sort()
    >>> l
    [2, 3, 'abc']
    >>> l.append('aaa')
    >>> l.sort()
    >>> l
    [2, 3, 'aaa', 'abc']

Dictionaries
------------

A dictionary represents a finite set of objects indexed by nearly arbitrary values.

Also known as a *map* or *hashtable* in other languages.

    >>> employee = { 'name': 'Balazs Szekely', 'login': 'bszekely', 'password': 'password' }
    >>> employee
    {'login': 'bszekely', 'password': 'password', 'name': 'Balazs Szekely'}
    >>> employee['name']
    'Balazs Szekely'
    >>> employee['login']
    'bszekely'
    >>> employee['password']
    'password'
    >>> employee['pass']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'pass'
    >>> employee.get('pass', 'n/a')
    'n/a'
    >>> employee['position'] = 'manager'
    >>> employee
    {'position': 'manager', 'login': 'bszekely', 'password': 'password', 'name': 'Balazs Szekely'}

The efficient implementation of dictionaries requires a key’s hash value to remain constant, so mutable data types are not acceptable as dictionary keys.

Byte arrays
-----------

    >>> f = file('/etc/issue')
    >>> f
    <open file '/etc/issue', mode 'r' at 0x2165030>
    >>> contents = f.read()
    >>> contents
    'Ubuntu 12.04.4 LTS \\n \\l\n\n'
    >>> b = bytearray(contents)
    >>> b
    bytearray(b'Ubuntu 12.04.4 LTS \\n \\l\n\n')

In Python 2, byte arrays behave like a mutable ``str``::

    >>> contents[0] = '.'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'str' object does not support item assignment
    >>> b[0] = '.'
    >>> b
    bytearray(b'.buntu 12.04.4 LTS \\n \\l\n\n')

Sets
----

Sets represent unordered, finite sets of unique, immutable objects.

    >>> s = {1,2,3}
    >>> s
    set([1, 2, 3])
    >>> len(s)
    3
    >>> s.add(4)
    >>> s
    set([1, 2, 3, 4])
    >>> s.add(1)
    >>> s
    set([1, 2, 3, 4])
    >>> s.remove(3)
    >>> s
    set([1, 2, 4])

Common uses for sets are fast membership testing, removing duplicates from a sequence, and computing mathematical operations such as intersection, union, difference, and symmetric difference.

    >>> s = {1,2,3}
    >>> u = {3,4}
    >>> 2 in s
    True
    >>> 2 in u
    False
    >>> set([1,2,3,2,5,3,4,2,5,1])
    set([1, 2, 3, 4, 5])

    >>> s.intersection(u)
    set([3])
    >>> s&u
    set([3])

    >>> s.union(u)
    set([1, 2, 3, 4])
    >>> s|u
    set([1, 2, 3, 4])

    >>> s.difference(u)
    set([1, 2])
    >>> s-u
    set([1, 2])

    >>> s.symmetric_difference(u)
    set([1, 2, 4])
    >>> s^u
    set([1, 2, 4])

Frozenset is the immutable (and therefore hashable) version of set:

    >>> ALLOWED_SCHEMES = frozenset(['http', 'https', 'ftp', 'ftps'])

