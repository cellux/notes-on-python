Functions
=========

Defining functions
------------------

A function definition creates a function object and binds it into the current namespace::


    def isleap(year):
        """Return True for leap years, False for non-leap years."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

The body of the created function 
will be executed when the function is called::

   >>> isleap(2000)
   True

Default parameter values
------------------------

::

    def escape(s, quote=None):
        '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true, the quotation mark character (")
        is also translated.'''
        s = s.replace("&", "&amp;") # Must be done first!
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        if quote:
            s = s.replace('"', "&quot;")
        return s

For a parameter with a default value, the corresponding argument may be omitted from a call, in which case the parameter’s default value is substituted.

If a parameter has a default value, all following parameters must also have a default value.

.. warning:: **Default parameter values are evaluated when the function definition is executed.**

   This means that the expression is evaluated only once - when the function is defined - and that the same “pre-computed” value is used for each call::

    >>> def a():
    ...     print "a executed"
    ...     return []
    ... 
    >>>            
    >>> def b(x=a()):
    ...     x.append(5)
    ...     print x
    ... 
    a executed
    >>> b()
    [5]
    >>> b()
    [5, 5]

   Sometimes, this behavior can be useful::

     def foo(i, j, cache={}):
         if (i, j) not in cache:
             cache[(i, j)] = expensive_operation(i, j)
         return cache[(i, j)]

Semantics of a function call
----------------------------

Upon a function call, all argument expressions are evaluated from left to right and then passed to the function as arguments::

  >>> def f(a,b): return a+b
  ... 
  >>> import math
  >>> f(math.sin(0),math.cos(0))
  1.0

If we call the function with more or less arguments than defined in the format parameter list, we get a ``TypeError``::

  >>> def f(a,b): return a+b
  ... 
  >>> f(1)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: f() takes exactly 2 arguments (1 given)
  >>> f(1,2,3)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: f() takes exactly 2 arguments (3 given)

The arguments to be passed can be also specified by name::

  >>> f(b=5,a=3)
  8

If a positional argument has been already assigned and we try to assign it again with a keyword argument, we get a ``TypeError``::

  >>> f(3,a=5)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: f() got multiple values for keyword argument 'a'

Otherwise, we can freely mix the two::

  >>> f(3,b=5)
  8

The only rule is that positional arguments must come first::

  >>> f(b=5,3)
    File "<stdin>", line 1
  SyntaxError: non-keyword arg after keyword arg

If a parameter has a default value, it can be omitted from the call::

  >>> def f(a,b,c=8): return a+b+c
  ... 
  >>> f(1,2,5)
  8
  >>> f(1,2)
  11

If a parameter has a default value, all following parameters must also have a default value::

  >>> def f(a,b,c=5,d): return a+b+c+d
  ... 
    File "<stdin>", line 1
  SyntaxError: non-default argument follows default argument

Excess positional arguments can be taken by declaring a formal parameter named ``*identifier``::

  >>> def f(a,b,*args): return a+b+sum(args)
  ... 
  >>> f(1,2,3,4,5,6)
  21

A real-world example::

    import sys

    def _l(prefix, template, *args):
        sys.stdout.write(str.format(prefix + template, *args))
        sys.stdout.write("\n")
        sys.stdout.flush()
    
    def log(template, *args):
        _l("===> ", template, *args)
    
    def die(template, *args):
        _l("ERROR ===> ", template, *args)
        raise RuntimeError("Jenkins build failed")

::

    >>> log("Hello {}, have a {} day.", 'Sauron', 'nice')
    ===> Hello Sauron, have a nice day.

Excess keyword arguments can be taken by declaring a formal parameter named ``**identifier``::

  >>> import re
  >>> def log(template, **vars):
  ...     print(re.sub(r'\$\{([^}]+)\}', lambda m: vars[m.group(1)], template))
  ... 
  >>> log("Hello ${name}, we have a beautiful ${day}.", name='Joe', day='Friday')
  Hello Joe, we have a beautiful Friday.

If there are no excess keyword arguments, the ``vars`` argument will be an empty dictionary (``{}``).

Another example::

    import subprocess

    def find(*args, **kwargs):
        """Execute find with given args, return output as a list of lines.
    
        Key-value pairs in kwargs are appended as `-key value` to find's
        command line.
    
        If find output was empty, return the empty list.
        """
        args = list(map(str, args))
        for k,v in kwargs.items():
            args.extend(['-'+k, str(v)])
        output = subprocess.check_output(['find']+args, universal_newlines=True)
        return output.splitlines()

::

   >>> find('.', maxdepth=1, name='*.py')
   ['./country-codes.py', './age.py', './png.py', './csv.py', './echo.py', './sublist.py', './check_heartbleed.py']

If the syntax ``*expression`` appears in the function call (as one of the arguments), ``expression`` must evaluate to an *iterable*. Elements from this iterable are treated as if they were additional positional arguments::

  >>> def define_translation(en_text, hu_text, de_text, es_text, it_text):
  ...     pass
  ... 
  >>> translations = {'apple':{'hu':'alma','de':'Apfel','es':'manzana','it':'mela'}}
  >>> for en_text, t in translations.items():
  ...     define_translation(en_text, *[t[k] for k in ('hu','de','es','it')])
  ... 

If the syntax ``**expression`` appears in the function call (as one of the arguments), ``expression`` must evaluate to a *mapping*, the contents of which are treated as additional keyword arguments::

    >>> 'Hello {name}, how are you?'.format(name='Joe')
    'Hello Joe, how are you?'

::

    from datetime import date

    def format_date(template, d=None):
        if d is None:
            d = date.today()
        template_vars = {
            'year': d.year,
            'month': d.month,
            'monthname': ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[d.month-1],
            'day': d.day,
            'weekday': d.weekday(),
            'weekdayname': ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')[d.weekday()],
        }
        return template.format(**template_vars)

::

    >>> format_date('{monthname} {day}, {year}, {weekdayname}'))
    May 9, 2014, Fri

In the case of a keyword appearing in both the ``**expression`` and as an explicit keyword argument, a ``TypeError`` exception is raised.

Lambda expressions
------------------

Lambda expressions evaluate to anonymous function objects::

    >>> import os
    >>> filelist = os.listdir('/')
    >>> filelist
    ['local', 'var', 'initrd.img', 'sbin', 'vmlinuz', 'boot', 'root', 'logs',
     'opt', '.rpmdb', 'tmp', 'run', 'srv', 'share', 'incoming', 'lib', 'dev', 
     'lost+found', 'home', 'initrd.img.old', 'mnt', 'proc', 'usr', 'media',
     'vmlinuz.old', 'lib32', 'build', '.gem', 'nap7', 'selinux', 'lib64',
     'etc', 'bin', 'cdrom', 'sys']
    >>> filelist.sort(key=lambda a: a.lower())
    >>> filelist
    ['.gem', '.rpmdb', 'bin', 'boot', 'build', 'cdrom', 'dev', 'etc', 'home',
     'incoming', 'initrd.img', 'initrd.img.old', 'lib', 'lib32', 'lib64',
     'local', 'logs', 'lost+found', 'media', 'mnt', 'nap7', 'opt', 'proc',
     'root', 'run', 'sbin', 'selinux', 'share', 'srv', 'sys', 'tmp', 'usr',
     'var', 'vmlinuz', 'vmlinuz.old']

We could define a separate function as well::

    >>> def call_lower(a): return a.lower()
    ... 
    >>> filelist.sort(key=call_lower)

but a lambda expression is more concise.

Nested functions
----------------

::

    import os, re

    def read_properties(path, resolve_vars_from={}):
        """Parse the property file at `path` and return the key-value pairs in a dict.
    
        ${...} style references are resolved using the following sources:
    
        1. properties defined earlier in the same file
        2. properties defined in the `resolve_vars_from` dictionary
        3. environment variables
        """
        props = {}
        with open(path) as f:
            def resolve_var(m):
                varname = m.group(1)
                if varname in props:
                    return props[varname]
                elif varname in resolve_vars_from:
                    return resolve_vars_from[varname]
                else:
                    return os.getenv(varname)
            def is_comment(line):
                return re.match(r'\s*#', line)
            for k,v in (line.split('=',1)
                        for line in f
                        if not is_comment(line) and '=' in line):
                k = k.strip()
                v = v.strip()
                v = re.sub(r'\$\{([^}]+)\}', resolve_var, v)
                props[k] = v
        return props

Example contents of a property file::

    SHARE=${HOME}/share
    BUILDDIR=${WORKSPACE}/.build
    PKGDIR=${BUILDDIR}/packages

Example invocation when the current working directory is ``/home/rb`` and the ``WORKSPACE`` environment variable is set to ``/tmp``::

    >>> read_properties('build.properties', {})
    {'SHARE': '/home/rb/share', 'BUILDDIR': '/tmp/.build', 'PKGDIR': '/tmp/.build/packages'}

Closures
--------

::

    # create_tempfile.py

    import os, atexit
    from random import randint
    
    def create_tempfile():
        pid = os.getpid()
        while True:
            random_digits = ''.join(chr(ord('0')+randint(0,9)) for x in range(16))
            path = '/tmp/{}-{}.tmp'.format(pid, random_digits)
            if not os.path.exists(path): break
        f = open(path, "w+")
        def cleanup():
            print "Closing and removing temp file: {}".format(path)
            f.close()
            if os.path.exists(path):
                os.unlink(path)
        atexit.register(cleanup)
        return f

::

    # create_tempfile_test.py

    from create_tempfile import create_tempfile

    f = create_tempfile()
    f.write("hello\n")

    raise RuntimeError("boom")

Running the test::

    rb@sw-hubu-1143:~/tmp$ python create_tempfile_test.py 
    Traceback (most recent call last):
      File "create_tempfile_test.py", line 8, in <module>
        raise RuntimeError("boom")
    RuntimeError: boom
    Closing and removing temp file: /tmp/25054-2001266244839515.tmp

Sublist unpacking
-----------------

    >>> a=5
    >>> b=3
    >>> c=8
    >>> x,y,z = b,a,c
    >>> x
    3
    >>> y
    5
    >>> z
    8

::

    >>> x,(y,z) = b,a,c
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: too many values to unpack
    >>> l = [c,a]
    >>> (x,y),z = l,b
    >>> x
    8
    >>> y
    5
    >>> z
    3

::

   >>> def f(x,(y,z),a):
   ...     print 'x={}, y={}, z={}, a={}'.format(x,y,z,a)
   ...
   >>> f(1,[5,8],3)
   x=1, y=5, z=8, a=3

Anatomy of a function
---------------------

::

    def fib(n):
        """Return the Nth Fibonacci number."""
        if n == 0 or n == 1:
            return 1
        else:
            return fib(n-1) + fib(n-2)

::

    >>> import profile
    >>> profile.run("print fib(20)")
    10946
             21894 function calls (4 primitive calls) in 0.088 seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 :0(setprofile)
      21891/1    0.088    0.000    0.088    0.088 <stdin>:1(fib)
            1    0.000    0.000    0.088    0.088 <string>:1(<module>)
            1    0.000    0.000    0.088    0.088 profile:0(print fib(20))
            0    0.000             0.000          profile:0(profiler)
    
    
    >>> profile.run("print fib(30)")
    1346269
             2692540 function calls (4 primitive calls) in 12.857 seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 :0(setprofile)
    2692537/1   12.857    0.000   12.857   12.857 <stdin>:1(fib)
            1    0.000    0.000   12.857   12.857 <string>:1(<module>)
            1    0.000    0.000   12.857   12.857 profile:0(print fib(30))
            0    0.000             0.000          profile:0(profiler)

::

    def memoize(f):
        cache = {}
        def g(x):
            if x not in cache:
                cache[x] = f(x)
            return cache[x]
        return g

    fib = memoize(fib)

::

    >>> profile.run("print fib(100)")
    573147844013817084101
             303 function calls (5 primitive calls) in 0.008 seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 :0(setprofile)
        101/1    0.004    0.000    0.008    0.008 <stdin>:1(fib)
        199/1    0.004    0.000    0.008    0.008 <stdin>:3(g)
            1    0.000    0.000    0.008    0.008 <string>:1(<module>)
            1    0.000    0.000    0.008    0.008 profile:0(print fib(100))
            0    0.000             0.000          profile:0(profiler)

Properties of function objects
##############################

::

    import time
    
    def memoize(f, timeout=0):
        cache = {}
        def g(x):
            now = time.time()
            if timeout and x in cache:
                value, ctime = cache[x]
                if (now - ctime) > timeout:
                    del cache[x]
            if x not in cache:
                cache[x] = (f(x), now)
            return cache[x]
        return g

::

    >>> memoize
    <function memoize at 0x7f26b46f17d0>
    >>> dir(memoize)
    ['__call__', '__class__', '__closure__', '__code__', '__defaults__',
     '__delattr__', '__dict__', '__doc__', '__format__', '__get__',
     '__getattribute__', '__globals__', '__hash__', '__init__', '__module__',
     '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
     '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
     'func_closure', 'func_code', 'func_defaults', 'func_dict',
     'func_doc', 'func_globals', 'func_name']
    >>> memoize.__name__
    'memoize'
    >>> memoize.__module__
    '__main__'
    >>> memoize.__class__
    <type 'function'>
    >>> memoize.__code__
    <code object memoize at 0x7f26b46e7eb0, file "<stdin>", line 1>
    >>> memoize.__defaults__
    (0,)
    >>> memoize.__globals__
    {'profile': <module 'profile' from '/usr/lib/python2.7/profile.pyc'>,
     '__builtins__': <module '__builtin__' (built-in)>,
     '__package__': None,
     'fib': <function g at 0x7f26b46ffed8>,
     'time': <module 'time' (built-in)>,
     '__name__': '__main__',
     'memoize': <function memoize at 0x7f26b46ff9b0>,
     '__doc__': None}

::

   >>> co = memoize.__code__
   >>> dir(co)
   ['__class__', '__cmp__', '__delattr__', '__doc__', '__eq__', '__format__',
    '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__',
    '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
    '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename',
    'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name',
    'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames']
   >>> co.co_name # function name
   'memoize'
   >>> co.__class__
   <type 'code'>
   >>> co.co_code # sequence of bytecode instructions
   'i\x00\x00\x89\x00\x00\x87\x02\x00\x87\x00\x00\x87\x01\x00f\x03\x00d\x01\x00\x86\x00\x00}\x02\x00|\x02\x00S'
   >>> co.co_argcount # number of positional arguments
   2
   >>> co.co_cellvars # names of local variables referenced by nested functions
   ('cache', 'timeout', 'f')
   >>> co.co_freevars # names of free variables
   ()
   >>> co.co_consts # literals used by the bytecode (first is docstring)
   (None, <code object g at 0x7f26b46e7db0, file "<stdin>", line 3>)
   >>> co.co_names # names used by the bytecode
   ()
   >>> co.co_filename
   '<stdin>'
   >>> co.co_nlocals # number of local variables (including arguments)
   3
   >>> co.co_varnames # name of local variables (starting with arguments)
   ('f', 'timeout', 'g')
