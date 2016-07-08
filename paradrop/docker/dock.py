
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
