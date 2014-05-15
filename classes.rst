Classes
=======

::

    from datetime import date

    class Person(object):
        """This is the Person class."""
        x = 5
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
            bonus_multiplier = (age-25)//5 if age >= 30 else 0
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

Anatomy of a class
------------------

    >>> Person
    <class '__main__.Person'>
    >>> dir(Person)
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__',
     '__getattribute__', '__hash__', '__init__', '__module__',
     '__new__', '__reduce__', '__reduce_ex__', '__repr__',
     '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
     '__weakref__', 'age', 'x']
    >>> dir(Employee)
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__',
     '__getattribute__', '__hash__', '__init__', '__module__',
     '__new__', '__reduce__', '__reduce_ex__', '__repr__',
     '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
     '__weakref__', 'age', 'salary', 'x']
    >>> Person.__class__
    <type 'type'>
    >>> Employee.__class__
    <type 'type'>
    >>> Person.__bases__
    (<type 'object'>,)
    >>> Employee.__bases__
    (<class '__main__.Person'>,)
    >>> Person.__doc__
    'This is the Person class.'
    >>> Employee.__doc__
    >>> Person.__module__
    '__main__'
    >>> Person.x
    5
    >>> Employee.x
    5
    >>> Person.__dict__
    dict_proxy({'__module__': '__main__',
                'age': <function age at 0xb7277614>,
                '__dict__': <attribute '__dict__' of 'Person' objects>,
                'x': 5,
                '__weakref__': <attribute '__weakref__' of 'Person' objects>,
                '__doc__': 'This is the Person class.',
                '__init__': <function __init__ at 0xb7271e2c>})
    >>> Employee.__dict__
    dict_proxy({'salary': <function salary at 0xb7277224>,
                '__module__': '__main__',
                '__doc__': None})
    >>> Person.__init__
    <unbound method Person.__init__>
    >>> Person.age
    <unbound method Person.age>
    >>> Employee.salary
    <unbound method Employee.salary>

Unbound methods
---------------

     >>> Person.age
     <unbound method Person.age>
     >>> dir(Person.age)
     ['__call__', '__class__', '__cmp__', '__delattr__', '__doc__',
      '__format__', '__func__', '__get__', '__getattribute__',
      '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__',
      '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__',
      '__subclasshook__', 'im_class', 'im_func', 'im_self']
     >>> Person.age.im_class
     <class '__main__.Person'>
     >>> Person.age.im_func
     <function age at 0xb7277614>
     >>> Person.age.im_self
     >>> Person.age(rb)
     38

Anatomy of a class instance
---------------------------

    >>> rb
    <__main__.Employee object at 0xb728244c>
    >>> dir(rb)
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__',
     '__getattribute__', '__hash__', '__init__', '__module__',
     '__new__', '__reduce__', '__reduce_ex__', '__repr__',
     '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
     '__weakref__', 'age', 'birth_date', 'name', 'salary', 'x']
    >>> rb.__class__
    <class '__main__.Employee'>
    >>> rb.__dict__
    {'birth_date': datetime.date(1975, 8, 24), 'name': u'Ruzsa Bal\xe1zs'}
    >>> rb.x
    5
    >>> rb.age
    <bound method Employee.age of <__main__.Employee object at 0xb728244c>>
    >>> rb.salary
    <bound method Employee.salary of <__main__.Employee object at 0xb728244c>>

Class instances can be extended with new properties at any time::

    >>> rb.height = 175
    >>> rb.__dict__
    {'birth_date': datetime.date(1975, 8, 24),
     'name': u'Ruzsa Bal\xe1zs',
     'height': 175}

Bound methods
-------------

    >>> rb.age
    <bound method Employee.age of <__main__.Employee object at 0xb728244c>>
    >>> rb.age is Person.age
    False
    >>> rb.age is Employee.age
    False
    >>> dir(rb.age)
    ['__call__', '__class__', '__cmp__', '__delattr__', '__doc__',
     '__format__', '__func__', '__get__', '__getattribute__', '__hash__',
     '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
     '__self__', '__setattr__', '__sizeof__', '__str__',
     '__subclasshook__', 'im_class', 'im_func', 'im_self']
    >>> rb.age.im_class
    class '__main__.Employee'
    >>> rb.age.im_func
    <function age at 0xb7277614>
    >>> rb.age.im_self
    <__main__.Employee object at 0xb728244c>

::

    >>> rb.age()
    38
    >>> f = rb.age
    >>> f()
    38

::

    >>> class KernelVersion(object):
    ...    f = rb.age
    ... 
    >>> KernelVersion.f()
    38
    >>> k = KernelVersion()
    >>> k.f()
    38

Using super()
-------------

Static methods
--------------

Class methods
-------------

