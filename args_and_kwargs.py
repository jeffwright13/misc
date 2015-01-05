'''
*args and **kwargs notation

*args (typically said "star-args") and **kwargs (stars can be implied by saying "kwargs", but be explicit with "double-star kwargs") are common idioms of Python for using the * and ** notation. These specific variable names aren't required (e.g. you could use *foos and **bars), but a departure from convention is likely to enrage your fellow Python coders.

We typically use these when we don't know what our function is going to receive or how many arguments we may be passing, and sometimes even when naming every variable separately would get very messy and redundant (but this is a case where usually explicit is better than implicit).

Example 1  -  foo()

The following function describes how they can be used, and demonstrates behavior. Note the named b argument will be consumed by the second positional argument before.
'''
def foo(a, b=10, *args, **kwargs):
    '''
    This function takes required argument a, not-required keyword
    argument b, and any number of unknown positional arguments and
    keyword arguments after that.
    '''

    print('a is a required argument, and its value is {0}'.format(a))

    print('b is not required; its default value is 10; its actual value is {0}'.format(b))

    # We can inspect the unknown arguments that were passed.
    #  -> args:
    print('args is of type {0} and length {1}'.format(type(args), len(args)))
    for arg in args:
        print('unknown arg: {0}'.format(arg))

    #  -> kwargs:
    print('kwargs is of type {0} and length {1}'.format(type(kwargs), len(kwargs)))
    for kw, arg in kwargs.items():
        print('unknown kwarg - kw: {0}, arg: {1}'.format(kw, arg))
        
    # But we don't have to know anything about them in order
    # to pass them to other functions:
    print('Either args or kwargs can be passed without knowing what they are:')
    # max can take two or more positional args: max(a, b, c...)
    print('e.g. max(a, b, *args) \n{0}'.format(max(a, b, *args))) 
    kweg = 'dict({0})'.format( # named args same as unknown kwargs
      ', '.join('{k}={v}'.format(k=k, v=v) 
                             for k, v in sorted(kwargs.items())))
    print('e.g. dict(**kwargs) (same as {kweg}) returns: \n{0}'.format(
      dict(**kwargs), kweg=kweg))

'''
We can check the online help for the function's signature, with help(foo), which tells us

foo(a, b=10, *args, **kwargs)
Let's call this function with foo(1, 2, 3, 4, e=5, f=6, g=7)

which prints:

a is a required argument, and its value is 1
b not required, its default value is 10, actual value: 2
args is of type <type 'tuple'> and length 2
unknown arg: 3
unknown arg: 4
kwargs is of type <type 'dict'> and length 3
unknown kwarg - kw: e, arg: 5
unknown kwarg - kw: g, arg: 7
unknown kwarg - kw: f, arg: 6
Args or kwargs can be passed without knowing what they are.
e.g. max(a, b, *args) 
4
e.g. dict(**kwargs) (same as dict(e=5, f=6, g=7)) returns: 
{'e': 5, 'g': 7, 'f': 6}
'''



'''
Example 2 - bar()

We can also call it using another function, into which we just provide a:
'''
def bar(a):
    b, c, d, e, f = 2, 3, 4, 5, 6
    # dumping every local variable into foo as a keyword argument 
    # by expanding the locals dict:
    foo(**locals()) 

'''
bar(100) prints:

a is a required argument, and its value is 100
b not required, its default value is 10, actual value: 2
args is of type <type 'tuple'> and length 0
kwargs is of type <type 'dict'> and length 4
unknown kwarg - kw: c, arg: 3
unknown kwarg - kw: e, arg: 5
unknown kwarg - kw: d, arg: 4
unknown kwarg - kw: f, arg: 6
Args or kwargs can be passed without knowing what they are.
e.g. max(a, b, *args) 
100
e.g. dict(**kwargs) (same as dict(c=3, d=4, e=5, f=6)) returns: 
{'c': 3, 'e': 5, 'd': 4, 'f': 6}
'''



'''
Example 3: practical usage in decorators

OK, so maybe we're not seeing the utility yet. So imagine you have several functions with redundant code before and/or after the differentiating code. The following named functions are just pseudo-code for illustrative purposes.

def foo(a, b, c, d=0, e=100):
    # imagine this is much more code than a simple function call
    preprocess() 
    differentiating_process_foo(a,b,c,d,e)
    # imagine this is much more code than a simple function call
    postprocess()

def bar(a, b, c=None, d=0, e=100, f=None):
    preprocess()
    differentiating_process_bar(a,b,c,d,e,f)
    postprocess()

def baz(a, b, c, d, e, f):
    ... and so on
We might be able to handle this differently, but we can certainly extract the redundancy with a decorator, and so our below example demonstrates how *args and **kwargs can be very useful:

def decorator(function):
    """function to wrap other functions with a pre- and postprocess"""
    @functools.wraps(function) # applies module, name, and docstring to wrapper
    def wrapper(*args, **kwargs):
        # again, imagine this is complicated, but we only write it once!
        preprocess()
        function(*args, **kwargs)
        postprocess()
    return wrapper
And now every wrapped function can be written much more succinctly, as we've factored out the redundancy:

@decorator
def foo(a, b, c, d=0, e=100):
    differentiating_process_foo(a,b,c,d,e)

@decorator
def bar(a, b, c=None, d=0, e=100, f=None):
    differentiating_process_bar(a,b,c,d,e,f)

@decorator
def baz(a, b, c=None, d=0, e=100, f=None, g=None):
    differentiating_process_baz(a,b,c,d,e,f, g)

@decorator
def quux(a, b, c=None, d=0, e=100, f=None, g=None, h=None):
    differentiating_process_quux(a,b,c,d,e,f,g,h)
And by factoring out our code, which *args and **kwargs allows us to do, we reduce lines of code, improve readability and maintainability, and have sole canonical locations for the logic in our program. If we need to change any part of this structure, we have one place in which to make each change.
'''