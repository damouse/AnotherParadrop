
import json
import threading
import Foo

counter = 1


def run(*a):
    global counter
    counter += 1

    print Foo.doSomething("this is patrick")

    print "PY: invocation", a, counter
    return "Hello from python!"


'''
Hypothetically, what needs to get done to have a go-core interface up with python.

    - Go serialization and deserialization, primitive types: int, bool, float, double, slice, map
        - Have to brute-force. Unless there's a reflection lib out there...?
    - Go method indexing, either through C or Go
        - Make an array of strings on the go side, have C pass them in 
        - Can the target methods just be labeled as "extern" in the header? That would be easy....
    - Python caller implementation.
        - If many-methods, then less of a problem.
        - If single caller, easier with a little class attr trickery


    (this is lower priority)
    - Core injection, either by swizzling a package or an object thats passed in.
        - If there's only one method on the core (look up map) this is easier to mock out with a python obj
        - If there's a bunch and shits calling it from everywhere then it will be hard to decouple. Maybe a later problem??

'''