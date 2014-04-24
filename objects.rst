Objects
=======

Everything is an object (even numbers):

    >>> 5.bit_length()
      File "<stdin>", line 1
        5.bit_length()
                   ^
    SyntaxError: invalid syntax

    >>> (5).bit_length()
    3

Objects are stored on the heap.

Every object has an *identity*, a *type* and a *value*.

An object’s identity never changes once it has been created; you may think of it as the object’s address in memory. The ``is`` operator compares the identity of two objects; the ``id()`` function returns an integer representing its identity.

    >>> id(5)
    10717016
    >>> id(6)
    10716992
    >>> 5 is 5
    True
    >>> 5 is 3
    False
    >>> 5 is 3+2
    True
    >>> "abc" is "abc"
    True
    >>> "abc" is "ab"+"c"
    True
    >>> "abc" is ("ab" "c")
    True

The ``type()`` function returns an object’s type (which is an object itself). Like its identity, an object’s type is also unchangeable.

    >>> type(None)
    <type 'NoneType'>
    >>> type(True)
    <type 'bool'>
    >>> type(False)
    <type 'bool'>
    >>> type(5)
    <type 'int'>
    >>> type(5.5)
    <type 'float'>
    >>> type(5.5j)
    <type 'complex'>
    >>> type("abc")
    <type 'str'>
    >>> type(u"Árvíztűrő tükörfúrógép")
    <type 'unicode'>
    >>> type(b"abc")
    <type 'str'>
    >>> type((1,2,3))
    <type 'tuple'>
    >>> type([1,2,3])
    <type 'list'>
    >>> type(bytearray([0x40,0xfc,0x10]))
    <type 'bytearray'>
    >>> type({'a':5,'b':3})
    <type 'dict'>
    >>> type({1,2,3})
    <type 'set'>
    >>> type(frozenset([1,2,3]))
    <type 'frozenset'>

Objects whose value can change are said to be *mutable*; objects whose value is unchangeable once they are created are called *immutable*. An object’s mutability is determined by its type; for instance, numbers, strings and tuples are immutable, while dictionaries and lists are mutable.

Objects are never explicitly destroyed; however, when they become unreachable they may be *garbage-collected*. An implementation is allowed to postpone garbage collection or omit it altogether — it is a matter of implementation quality how garbage collection is implemented, as long as no objects are collected that are still reachable.

Some objects contain references to other objects; these are called *containers*. Examples of containers are tuples, lists and dictionaries.

