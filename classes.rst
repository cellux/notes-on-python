Classes
=======

::

    from datetime import date

    class Person(object):
        """This is the Person class."""
        def __init__(self, name, birth_date):
            self.name = name
            if not isinstance(birth_date, tuple) \
               or len(birth_date) != 3 \
               or not all(isinstance(x,int) for x in birth_date):
                raise ValueError("birth_date must be a tuple of three integers")
            y,m,d = birth_date
            self.birth_date = date(y,m,d)
        def age(self):
            delta = date.today() - self.birth_date
            return delta.days // 365

    class Employee(Person):
        def salary(self):
            """Calculate the employee's salary.

            From the age of 30, every employee is eligible of a bonus
            which starts at 1 peták and increases by 1 peták every
            five years."""
            age = self.age()
            base_salary = 10
            bonus_amount = 1
            bonus_multiplier = (age-30)//5 + 1 if age >= 30 else 0
            return base_salary + bonus_amount * bonus_multiplier

::

    >>> rb = Employee(u"Ruzsa Balázs", (1975,8,24))
    >>> rb.name
    u'Ruzsa Bal\xe1zs'
    >>> rb.birth_date
    datetime.date(1975, 8, 24)
    >>> rb.age()
    38
    >>> rb.salary()
    12

super
-----

Let's make the salary of an employee overrideable::

    class Employee(Person):
        base_salary = 10
        bonus_after = 30 # years
        bonus_amount = 1
        def __init__(self, name, birth_date, salary=None):
            super(Employee, self).__init__(name, birth_date)
            self._salary = salary
        def get_salary(self):
            """Calculate the employee's salary.
    
            From the age of 30, every employee is eligible of a bonus
            which starts at 1 peták and increases by 1 peták every
            five years."""
            if self._salary:
                return self._salary
            else:
                age = self.age()
                if age >= self.bonus_after:
                    bonus_multiplier = (age - self.bonus_after) // 5 + 1
                else:
                    bonus_multiplier = 0
                return self.base_salary + self.bonus_amount * bonus_multiplier
        def set_salary(self, new_salary):
            self._salary = new_salary
        salary = get_salary # for backwards compatibility

::

    >>> rb = Employee(u"Ruzsa Balázs", (1975,8,24))
    >>> rb.get_salary()
    12
    >>> rb.set_salary(100)
    >>> rb.get_salary()
    100

``super(cls, obj)`` returns a proxy object which when queried for an attribute ``x`` returns the attribute with this name from the nearest base class of ``cls`` in which the attribute can be found. When the returned attribute (usually a method) is called, ``obj`` will be used as the ``self`` argument.

.. note:: The algorithm of finding the nearest base class - called "C3 superclass linearization" or "Method Resolution Order" (MRO) - is described `here <https://www.python.org/download/releases/2.3/mro/>`_.

Bound and unbound methods
-------------------------

Unbound methods
###############

The variables and functions we create inside a class definition are stored within a dictionary inside the class object::

  >>> Person.__dict__
  dict_proxy({'__module__': '__main__',
              'age': <function age at 0x1d43578>,
              '__dict__': <attribute '__dict__' of 'Person' objects>,
              '__weakref__': <attribute '__weakref__' of 'Person' objects>,
              '__doc__': 'This is the Person class.',
              '__init__': <function __init__ at 0x1d43500>})
  >>> Employee.__dict__
  dict_proxy({'salary': <function get_salary at 0x1d43758>,
              'bonus_amount': 1,
              '__module__': '__main__',
              'set_salary': <function set_salary at 0x1d437d0>,
              'base_salary': 10,
              '__doc__': None,
              '__init__': <function __init__ at 0x1d436e0>,
              'get_salary': <function get_salary at 0x1d43758>})

When we retrieve a function object from the class (e.g. we say something like ``Person.age``), what we actually get is not the function object stored in ``Person.__dict__``, but a dynamically created proxy called an *unbound method*::

   >>> Person.__dict__['age']
   <function age at 0x1d43578>
   >>> Person.age
   <unbound method Person.age>

This wrapper, when called, forwards the call to the wrapped function object and also checks that the first argument of the call is an object of the class from which the function was retrieved::

   >>> age = Person.age
   >>> age()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: unbound method age() must be called with Person instance as first argument (got nothing instead)
   >>> age(rb)
   38

Objects of an ancestor class are not accepted (but descendants are)::

   >>> p = Person(u'Ruzsa Rebeka', (2004,12,1))
   >>> age = Employee.age
   >>> age(p)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: unbound method age() must be called with Employee instance as first argument (got Person instance instead)

An unbound method stores the class and the function which it should forward to inside itself::

  >>> Person.age.im_class
  <class '__main__.Person'>
  >>> Person.age.im_func
  <function age at 0x1d43578>

Bound methods
#############

If we retrieve a function from an *instance* of the class, we get a *bound method*::

   >>> rb.age
   <bound method Employee.age of <__main__.Employee object at 0x1d41dd0>>

This method remembers not just the class and the function, but also the object from which it was retrieved from::

  >>> rb.age.im_class
  <class '__main__.Employee'>
  >>> rb.age.im_func
  <function age at 0x1d43578>
  >>> rb.age.im_self
  <__main__.Employee object at 0x1d41dd0>

When such a bound method is called, it forwards the call to the stored function object and passes the stored ``im_self`` as the first argument::

  >>> age = rb.age
  >>> age()
  38

Class methods
-------------

Sometimes we want to define a method which operates on the class itself - a good example is a factory method::

    # a possible implementation of dict.fromkeys:
    
    class dict(object):
        # ...
        def fromkeys(cls, iterable, value=None):
            '''dict.fromkeys(S[, v]) -> New dictionary with keys from S.
            If not specified, the value defaults to None.
    
            '''
            self = cls()
            for key in iterable:
                self[key] = value
            return self
        # ...

The problem with this definition::

  >>> dict.fromkeys(['a','b','c'])
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: unbound method fromkeys() must be called with dict instance as first argument (got list instance instead)

Perhaps we should add the class as the first argument?

  >>> dict.fromkeys(dict, ['a','b','c'])
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: unbound method fromkeys() must be called with dict instance as first argument (got type instance instead)

No, because ``dict.fromkeys`` now returns an unbound method which must be called with an instance of ``dict`` as the first argument.

The solution is to convert ``fromkeys`` into a *class method*::

    class dict(object):
        # ...
        def fromkeys(cls, iterable, value=None):
            '''dict.fromkeys(S[, v]) -> New dictionary with keys from S.
            If not specified, the value defaults to None.
    
            '''
            self = cls()
            for key in iterable:
                self[key] = value
            return self
        fromkeys = classmethod(fromkeys)
        # ...

Now, when we retrieve ``fromkeys`` from the class, instead of the usual unbound method, we get a *class method* which will insert the class we retrieved it from as the first argument when called::

    >>> dict.fromkeys(['a','b','c'])
    {'a': None, 'c': None, 'b': None}

Instead of calling classmethod explicitly, we could also use a *decorator*::

    @classmethod
    def fromkeys(cls, iterable, value=None):
        # ...

Static methods
--------------

Sometimes we have a function which conceptually belongs to the class, but doesn't actually access either the class or its instances.

Such a function may provide a service similar to the purpose of the class, or it may be a helper function used by some other methods of the class::

   class A(object):
      def helper():
         return 42
      def use_helper(self):
         print self.helper()

The problem is we cannot use this function in the expected way because it immediately turns into a bound (or unbound) method when we access it::

    >>> a = A()
    >>> a.use_helper()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 5, in use_helper
    TypeError: helper() takes no arguments (1 given)
    >>> A.helper()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unbound method helper() must be called with A instance as first argument (got nothing instead)

The solution is to convert the function into a *static method*::

   class A(object):
      def helper():
         return 42
      helper = staticmethod(helper)
      def use_helper(self):
         print self.helper()

A decorator also works::

   class A(object):
      @staticmethod
      def helper():
         return 42

Now we can use it as intended::

    >>> a = A()
    >>> a.use_helper()
    42
    >>> A.helper()
    42

Class attributes
----------------

The variables defined inside class ``C`` are stored in the dictionary ``C.__dict__``::

  >>> class C(object):
  ...   x = 5
  ...   def f(self): return 42
  ... 
  >>> C.__dict__
  dict_proxy({'__module__': '__main__',
              'f': <function f at 0x1d531b8>,
              '__dict__': <attribute '__dict__' of 'C' objects>,
              'x': 5,
              '__weakref__': <attribute '__weakref__' of 'C' objects>,
              '__doc__': None})

These variables (including the functions defined with ``def``) are called *class attributes*.

Class attributes are not visible (they are not in scope) inside the methods of the class::

  >>> class C(object):
  ...   x = 5
  ...   def f(self): return x
  ... 
  >>> c = C()
  >>> c.f()
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<stdin>", line 3, in f
  NameError: global name 'x' is not defined

They must be retrieved from either the class or the instance::

  >>> class C(object):
  ...   x = 5
  ...   def f1(self): return C.x
  ...   def f2(self): return self.x
  ... 
  >>> c = C()
  >>> c.f1()
  5
  >>> c.f2()
  5

Existing classes can be extended with new attributes at any time::

  >>> C.y = 10
  >>> C.__dict__
  dict_proxy({'f1': <function f1 at 0x15707d0>,
              '__module__': '__main__',
              'f2': <function f2 at 0x1570848>,
              'y': 10,
              '__dict__': <attribute '__dict__' of 'C' objects>,
              'x': 5,
              '__weakref__': <attribute '__weakref__' of 'C' objects>,
              '__doc__': None})

Attribute inheritance
#####################

Derived classes inherit attributes from their parents::

  >>> class D(C):
  ...   pass
  ... 
  >>> D.x
  5
  >>> d = D()
  >>> d.f1()
  5

They can also override them::

  >>> class D(C):
  ...   def f1(self): return self.x+10
  ... 
  >>> d = D()
  >>> d.x
  5
  >>> d.f1()
  15

Attribute lookup happens at run-time, *not* compile-time::

  >>> C.x = 12
  >>> D.x
  12
  >>> d.x
  12

Multiple inheritance
####################

  >>> class M(C,dict):
  ...   pass
  ... 
  >>> m = M()
  >>> m.x
  12
  >>> m['a'] = 5

The base classes are stored in the special attribute ``__bases__``::

  >>> M.__bases__
  (<class '__main__.C'>, <type 'dict'>)

The actual method resolution order is returned by ``mro()``::

  >>> M.mro()
  [<class '__main__.M'>, <class '__main__.C'>, <type 'dict'>, <type 'object'>]

Instance attributes
-------------------

    >>> class C(object):
    ...   x = 5
    ...   def __init__(self):
    ...     self.x = 42
    ... 
    >>> c = C()
    >>> c.x
    42
    >>> C.x
    5

Instance attributes are stored in the instance object's ``__dict__`` dictionary::

    >>> c.__dict__
    {'x': 42}

When a program tries to retrieve ``c.x``, Python looks for the attribute in the following places:

1. ``c.__dict__``
2. ``C.__dict__ for C in type(c).mro()``

Existing instances can be extended with new attributes at any time::

    >>> c.y = 10
    >>> c.__dict__
    {'y': 10, 'x': 42}
