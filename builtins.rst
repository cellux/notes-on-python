Builtins
========

*Builtins* are those objects which are bound in the global namespace of all modules.

This means they can be seen (resolved) everywhere - unless they are shadowed by a local variable with the same name.

.. note:: This page does not mention all builtins.

   Some of the builtin types for instance (``str``, ``int``, ``float``, ``set``, ``list``, ``file`` etc.) have been already discussed, so I won't describe them again.

   For a complete list of all builtins, type ``help(__builtins__)`` at a Python prompt.

bool
----

The ``bool`` class has two singleton instances: ``True`` and ``False``.

When you create an instance of ``bool`` - by invoking ``bool(x)`` -, the constructor determines the truth value of ``x`` and returns the corresponding singleton (either ``True`` or ``False``).

The following values are considered false:

* ``None``
* ``False``
* zero of any numeric type, e.g. ``0``, ``0L``, ``0.0``, ``0j``
* any empty sequence, e.g. ``''``, ``()``, ``[]``
* any empty mapping, e.g. ``{}``
* instances of user-defined classes, if the class defines a ``__nonzero__()`` or ``__len__()`` method, when that method returns the integer zero or bool value ``False``

All other values are considered true.

buffer
------

::

    import mmap, struct, contextlib, zlib

    class PNGError(Exception):
        pass

    def process_png_chunks(path, process_cb):
        with open(path) as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            with contextlib.closing(mm) as data:
                if data[0:8] != bytearray([137,80,78,71,13,10,26,10]):
                    raise PNGError("Invalid PNG signature")
                pos = 8
                while pos < len(data):
                    chunk_length = int(struct.unpack('>L', data[pos:pos+4])[0])
                    chunk_type = data[pos+4:pos+8]
                    chunk_data = buffer(data, pos+8, chunk_length)
                    chunk_crc = int(struct.unpack('>L', data[pos+8+chunk_length:pos+8+chunk_length+4])[0])
                    crc = zlib.crc32(chunk_type)
                    crc = zlib.crc32(chunk_data, crc)
                    if crc < 0: crc = (1<<32) + crc
                    if chunk_crc != crc:
                        raise PNGError("Invalid CRC in PNG file, in file={0:X}, expected={1:X}".format(chunk_crc, crc))
                    process_cb(chunk_type, chunk_data)
                    pos = pos+4+4+chunk_length+4
    
    def print_chunk_info(chunk_type, chunk_data):
        print "chunk: type={}, len={}".format(chunk_type, len(chunk_data))
    
    process_png_chunks('button.png', print_chunk_info)

::

   rb@sw-hubu-1143:~/tmp$ python png.py 
   chunk: type=IHDR, len=13
   chunk: type=PLTE, len=81
   chunk: type=tRNS, len=15
   chunk: type=IDAT, len=167
   chunk: type=IEND, len=0

bytearray
---------

::

   >>> bytearray([1,2,3,4,250])
   bytearray(b'\x01\x02\x03\x04\xfa')

   >>> bytearray(8)
   bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')

   >>> bytearray("hello, world")
   bytearray(b'hello, world')

   >>> s = u"Árvíztűrő tükörfúrógép"
   >>> bytearray(s, 'utf-8')
   bytearray(b'\xc3\x81rv\xc3\xadzt\xc5\xb1r\xc5\x91 t\xc3\xbck\xc3\xb6rf\xc3\xbar\xc3\xb3g\xc3\xa9p')
   >>> bytearray(s, 'latin2')
   bytearray(b'\xc1rv\xedzt\xfbr\xf5 t\xfck\xf6rf\xfar\xf3g\xe9p')

Byte arrays are mutable::

    >>> b = bytearray("hello, world")
    >>> b[4] = 'a'
    >>> b
    bytearray(b'hella, world')
    >>> b += '!'
    >>> b
    bytearray(b'hella, world!')

You can convert a hex string into a byte array using the ``fromhex()`` static method::

   >>> b = bytearray.fromhex('C381C3ADC5B1C591')
   >>> b
   bytearray(b'\xc3\x81\xc3\xad\xc5\xb1\xc5\x91')
   >>> b.decode('utf-8')
   u'\xc1\xed\u0171\u0151'

bytes
-----

Instances of the ``bytes`` type hold a sequence of bytes.

Equivalent to ``str`` in Python 2.

============== ============= =============
Concept        Python 2 type Python 3 type
============== ============= =============
byte string    str, bytes    bytes
unicode string unicode       str
============== ============= =============

Python 2::

  >>> type('Hello, world')
  <type 'str'>
  >>> type(b'Hello, world')
  <type 'str'>
  >>> type(u'Hello, world')
  <type 'unicode'>

Python 3::

  >>> type('Hello, world')
  <class 'str'>
  >>> type(b'Hello, world')
  <class 'bytes'>
  >>> type(u'Hello, world')
    File "<stdin>", line 1
      type(u'Hello, world')
                       ^
  SyntaxError: invalid syntax

dict
----

  >>> dict
  <type 'dict'>
  >>> dict()
  {}
  >>> dict({'a':5,'b':3})
  {'a': 5, 'b': 3}
  >>> {'a':5, 'b':3}
  {'a': 5, 'b': 3}
  >>> dict([('a',5),('b',3)])
  {'a': 5, 'b': 3}
  >>> dict(a=3,b=5)
  {'a': 3, 'b': 5}
  >>> dict.fromkeys(['a','b','c'])
  {'a': None, 'c': None, 'b': None}
  >>> dict.fromkeys(['a','b','c'], 8)
  {'a': 8, 'c': 8, 'b': 8}

Elements can be accessed and assigned via subscripting the dictionary::

  >>> d = {'a':5,'b':3}
  >>> d['a']
  5
  >>> d['c'] = 8
  >>> d
  {'a': 5, 'c': 8, 'b': 3}

If the key does not exist, Python raises a ``KeyError``::

  >>> d['z']
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  KeyError: 'z'

If you want to avoid the ``KeyError``, use the ``get(key, default=None)`` method::

  >>> d.get('z')
  >>> d.get('z', 'N/A')
  'N/A'

You may also use ``setdefault(key, default=None)`` which works like ``get()`` but also adds a new item (with value ``default``) to the dict if ``key`` does not exist yet::

  >>> d = {'a':5,'b':3}
  >>> d.setdefault('a',8)
  5
  >>> d.setdefault('b',8)
  3
  >>> d.setdefault('c',8)
  8
  >>> d
  {'a': 5, 'c': 8, 'b': 3}

You can check for the existence of a key with ``has_key(k)``::

  >>> d.has_key('a')
  True
  >>> d.has_key('z')
  False

You can get the keys, the values or both using the following methods::

  >>> d.keys()
  ['a', 'b']
  >>> d.values()
  [5, 3]
  >>> d.items()
  [('a', 5), ('b', 3)]

You can bulk-set keys and values using ``update()``::

  >>> d={'a':5,'b':3}
  >>> d.update(x=10,y=20,z=30)
  >>> d
  {'a': 5, 'y': 20, 'b': 3, 'z': 30, 'x': 10}

``update()`` also accepts any iterable (besides the keyword arguments)::

    import httplib, re
    
    countries = {}
    
    conn = httplib.HTTPConnection("www.geonames.org")
    conn.request('GET', "/countries/")
    res = conn.getresponse()
    if res.status == 200:
        countries.update(
          (m.group(1), m.group(5))
          for m in
          re.finditer(r'<tr><td><a name=".*"></a>(\w+)</td><td>(\w+)</td><td>(\d+)</td><td>(\w+)</td><td><a href="[^"]+">([^<]+)</a></td><td>([^<]+)</td><td class="rightalign">([0-9,.]+)</td><td class="rightalign">([0-9,.]+)</td><td>(\w+)</td></tr>', res.read()))
    
    for code,name in countries.iteritems():
        print("{}={}".format(code,name))

You can remove an element under a given key using ``pop(key, default)``::

  >>> d = {'a':5,'b':3}
  >>> d.pop('a')
  5
  >>> d
  {'b': 3}

You can remove all elements with ``clear()``::

  >>> d = {'a':5,'b':3}
  >>> d
  {'a': 5, 'b': 3}
  >>> d.clear()
  >>> d
  {}

enumerate
---------

    >>> for i,v in enumerate(['a','b','c']):
    ...   print('index={}, value={}'.format(i,v))
    ... 
    index=0, value=a
    index=1, value=b
    index=2, value=c

    >>> list(enumerate(['a','b','c']))
    [(0, 'a'), (1, 'b'), (2, 'c')]

    >>> list(enumerate(['a','b','c'], 5))
    [(5, 'a'), (6, 'b'), (7, 'c')]

reversed
--------

    >>> reversed(['a','b','c'])
    <listreverseiterator object at 0x1aa7a50>
    >>> list(reversed(['a','b','c']))
    ['c', 'b', 'a']

abs
---

    >>> abs(-5)
    5

all
---

::

    with open('/etc/passwd') as f:
        usernames = (line.split(':',1)[0] for line in f)
        if all(len(username) <= 16 for username in usernames):
            print "All usernames on this system have a length not greater than 16 characters."
        else:
            print "Some usernames on this system are longer than 16 characters."

any
---

::

    with open('/etc/passwd') as f:
        usernames = (line.split(':',1)[0] for line in f)
        if any(len(username) > 16 for username in usernames):
            print "Some usernames on this system are longer than 16 characters."
        else:
            print "All usernames on this system have a length not greater than 16 characters."

bin
---

Return the binary representation of an integer or long integer::

    >>> bin(129)
    '0b10000001'

callable
--------

    >>> callable(5)
    False
    >>> def f(): print 5
    ... 
    >>> f()
    5
    >>> callable(f)
    True
    >>> callable(callable)
    True
    >>> callable(bool)
    True

chr
---

    >>> chr(65)
    'A'
    >>> chr(255)
    '\xff'
    >>> chr(256)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: chr() arg not in range(256)

    >>> unichr(256)
    u'\u0100'

cmp
---

   cmp(...)
        cmp(x, y) -> integer
        
        Return negative if x<y, zero if x==y, positive if x>y.

>>> cmp(0,5)
-1
>>> cmp(5,5)
0
>>> cmp(5,0)
1

Works on any type which defines the ``__cmp__`` (or ``__lt__``, ``__le__``, ``__eq__``, ``__ne__``, ``__gt__``, ``__ge__``) special methods for its instances.

dir
---

If called without an argument, return the names in the current scope::

    >>> dir()
    ['__builtins__', '__doc__', '__name__', '__package__']
    >>> __builtins__
    <module '__builtin__' (built-in)>
    >>> __doc__
    >>> __name__
    '__main__'
    >>> __package__
    >>> a=5
    >>> dir()
    ['__builtins__', '__doc__', '__name__', '__package__', 'a']

Else, return an alphabetized list of names comprising (some of) the attributes of the given object, and of attributes reachable from it::

  >>> dir(__builtins__)
  ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException',
   'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError',
   'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError',
   'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
   'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
   'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented',
   'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning',
   'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError',
   'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
   'SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError',
   'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
   'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError',
   '_', '__debug__', '__doc__', '__import__', '__name__', '__package__',
   'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer',
   'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce',
   'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir',
   'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter',
   'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
   'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass',
   'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max',
   'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
   'print', 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload',
   'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted',
   'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr',
   'unicode', 'vars', 'xrange', 'zip']

divmod
------

    divmod(x, y) -> (quotient, remainder)
        Return the tuple ``((x-x%y)/y, x%y)``.

>>> divmod(13,5)
(2, 3)
>>> assert 13//5 == divmod(13,5)[0]
>>> assert 13%5 == divmod(13,5)[1]

filter
------

    >>> filter(lambda c: c in "aeiou", "Hello, world")
    'eoo'

Without using ``lambda``:

    >>> def is_vowel(c):
    ...     return c in "aeiou"
    ... 
    >>> filter(is_vowel, "Hello, world!")
    'eoo'

.. note:: Lambda expressions create anonymous functions:

   >>> is_vowel = lambda c: c in "aeiou"
   >>> is_vowel
   <function <lambda> at 0xa28500>

globals
-------

    globals() -> dictionary
        Return the dictionary containing the current scope's global variables.

>>> globals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}

Contrast with ``dir()``::

    >>> dir()
    ['__builtins__', '__doc__', '__name__', '__package__']

hex
---

Return the hexadecimal representation of an integer or long integer::

    >>> hex(49152)
    '0xc000'

id
--

    id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among simultaneously existing objects.  (Hint: it's the object's memory address.)

Interestingly, integers also have an unique identity (at least some of them)::

    >>> id(0)
    16078800
    >>> id(1)
    16078776
    >>> id(2)
    16078752

    >>> id(254)
    16084656
    >>> id(255)
    16084632
    >>> id(256)
    16084608

From 257 upwards, their identities dissolve and they all become one::

    >>> id(257)
    16362640
    >>> id(258)
    16362640
    >>> id(259)
    16362640

Based on this observation, one would think that the identity of let's say ``300`` and ``301`` are the same::

    >>> id(300)
    16362592
    >>> id(301)
    16362592

But the ``is`` operator tells us otherwise::

    >>> 300 is 301
    False

input
-----

::

   from datetime import date

   birth_year = input("Give me the year you were born: ")
   today_year = date.today().year
   print("You are about {} years old.".format(today_year - birth_year))

isinstance
----------

    isinstance(object, class-or-type-or-tuple) -> bool
        Return whether an object is an instance of a class or of a subclass thereof.

::

   >>> isinstance(0, int)
   True
   >>> isinstance(0, float)
   False
   >>> isinstance(0.0, float)
   True
   >>> isinstance(0, (int, float))
   True

Booleans are subclasses of ``int``::

  >>> isinstance(True, bool)
  True
  >>> isinstance(True, int)
  True

``str`` and ``unicode`` are separate types::

  >>> isinstance("abc", str)
  True
  >>> isinstance("abc", unicode)
  False
  >>> isinstance(u"abc", str)
  False
  >>> isinstance(u"abc", unicode)
  True

And both are subclasses of ``basestring``::

  >>> isinstance("abc", basestring)
  True
  >>> isinstance(u"abc", basestring)
  True

But ``str`` is not a ``basestring``::

  >>> isinstance(str, basestring)
  False

It's a ``type``::

  >>> isinstance(str, type)
  True

By the way, ``type`` is also a ``type``::

  >>> isinstance(type, type)
  True

issubclass
----------

    >>> issubclass(str, basestring)
    True

len
---

    >>> len("abc")
    3
    >>> len([1,2,3])
    3
    >>> len((1,2,3))
    3
    >>> len({'a':5,'b':3})
    2

locals
------

At the top level, ``locals()`` and ``globals()`` return the same dictionary::

  >>> locals()
  {'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}
  >>> globals()
  {'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}
  >>> globals() is locals()
  True

But classes and functions introduce a new namespace, so inside them, ``locals()`` returns a different dictionary::

  >>> class A(object):
  ...     x = 4
  ...     y = 56
  ...     print(locals())
  ... 
  {'y': 56, 'x': 4, '__module__': '__main__'}

  >>> def f():
  ...     x = 8
  ...     y = 10
  ...     print(locals())
  ... 
  >>> f()
  {'y': 10, 'x': 8}

map
---

    >>> range(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> map(lambda x: x**2, range(10))
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >>> map(lambda c: chr(ord(c)+1), 'HAL')
    ['I', 'B', 'M']

If more than one sequence is given, the first fn arg is called with an argument list consisting of the corresponding item of each sequence, substituting None for missing values when not all sequences have the same length::

  >>> map(lambda i,s: "{}. {}".format(i,s or '(empty)'), range(1,11), ["Joe","Bill","Steve","Dick"])
  ['1. Joe', '2. Bill', '3. Steve', '4. Dick', '5. (empty)', '6. (empty)', '7. (empty)', '8. (empty)', '9. (empty)', '10. (empty)']

max
---

::

    >>> from math import sin, radians
    >>> max(sin(radians(x)) for x in range(360))
    1.0

min
---

::

    >>> from math import cos, radians
    >>> min(cos(radians(x)) for x in range(360))
    -1.0

oct
---

Return the octal representation of an integer or long integer::

   >>> oct(15)
   '017'

open
----

    open(...)
        open(name[, mode[, buffering]]) -> file object

The ``buffering`` argument may have the following values:

===== =================================
Value Meaning
===== =================================
``0`` unbuffered
``1`` line buffered
``n`` buffered with buffer size = ``n``
===== =================================

ord
---

    >>> ord('a')
    97
    >>> ord('ő')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: ord() expected a character, but string of length 2 found
    >>> ord(u'ő')
    337

range
-----

    >>> range(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> range(0,10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> range(1,10)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> range(1,11)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> range(5,10)
    [5, 6, 7, 8, 9]
    >>> range(10,5)
    []
    >>> range(10,5,-1)
    [10, 9, 8, 7, 6]
    >>> range(10,5,-2)
    [10, 8, 6]
    >>> range(10,4,-2)
    [10, 8, 6]
    >>> range(10,3,-2)
    [10, 8, 6, 4]

There is also ``xrange()`` (Python 2 only), which is more efficient as it does not create a list in the background.

In Python 3, ``range()`` is the same as ``xrange()`` in Python 2.

round
-----

    >>> round(5.2)
    5.0
    >>> round(3.14519,2)
    3.15
    >>> round(123.14519,-1)
    120.0
    >>> round(123.14519,-2)
    100.0

sorted
------

    >>> sorted("Hello, world")
    [' ', ',', 'H', 'd', 'e', 'l', 'l', 'l', 'o', 'o', 'r', 'w']

    >>> def is_vowel(c):
    ...     return c in "aeiou"
    ... 
    >>> sorted("Hello, world", key=is_vowel)
    ['H', 'l', 'l', ',', ' ', 'w', 'r', 'l', 'd', 'e', 'o', 'o']

    >>> print(u''.join(sorted(u"Árvíztűrő tükörfúrógép")))
    fgkprrrrttvzÁéíóöúüőű

    >>> chars=u"aábcdeéfghiíjklmnoóöőpqrstuúüűvwxzy"
    >>> print(u''.join(sorted(u"Árvíztűrő tükörfúrógép", key=lambda c: chars.find(c.lower()))))
    Áéfgíkóöőprrrrttúüűvz

    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'hu_HU.UTF-8')
    'hu_HU.UTF-8'
    >>> locale.strcoll(u'é',u'e')
    2
    >>> locale.strcoll(u'e',u'é')
    -2
    >>> print(u''.join(sorted(u"Árvíztűrő tükörfúrógép", cmp=locale.strcoll)))
    Áéfgíkóöőprrrrttúüűvz

sum
---

    >>> sum(range(101))
    5050

unichr
------

Just like ``chr()`` but converts Unicode code points to the respective characters (= ``unicode`` objects of length 1)::

    >>> unichr(0x151)
    u'\u0151'
    >>> print(unichr(0x151))
    ő

zip
---

    >>> zip([1,2,3],['a','b','c'])
    [(1, 'a'), (2, 'b'), (3, 'c')]

    >>> zip([1,2,3],['a','b','c'],'hello, world')
    [(1, 'a', 'h'), (2, 'b', 'e'), (3, 'c', 'l')]

::

    #!/usr/bin/env python
    
    import sys, codecs, re, json
    
    def csv_to_json(path, encoding):
        def unquote(field):
            field = field.strip(' \t')
            for regex in (r'^"(.*)"$', r"^'(.*)'$"):
                m = re.search(regex, field)
                if m:
                     field = m.group(1)
                     break
            return field
        with codecs.open(path, encoding=encoding) as f:
            header = f.readline().strip()
            fieldnames = [unquote(h) for h in header.split(',')]
            rows = []
            for line in f:
                line = line.strip()
                fieldvalues = [unquote(f) for f in line.split(',')]
                rows.append(dict(zip(fieldnames, fieldvalues)))
        return rows
    
    if len(sys.argv) < 2:
        print "Usage: csv_to_json.py <csvpath> [<encoding>]"
    else:
        csv_path = sys.argv[1]
        csv_encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'
        csv_rows = csv_to_json(csv_path, csv_encoding)
        print(json.dumps(csv_rows, indent=True))
