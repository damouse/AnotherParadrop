#include "Python.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>

extern PyObject* callback(PyObject* arg);
extern PyObject* port(PyObject *self, PyObject *args);

// Get rid of this, use the manual exporting
static PyObject* Foo_doSomething(PyObject *self, PyObject *args){
    PyObject* objectsRepresentation = PyObject_Repr(args);
    const char* s = PyString_AsString(objectsRepresentation);
    printf("%s\n", s);

    callback(args);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef ModuleMethods[] = {
    {"doSomething", Foo_doSomething, METH_VARARGS, "doc string"},
    {"exporteed", port, METH_VARARGS, "doc string"},
    {NULL},
};

static void initialize_python () {

    if (Py_IsInitialized() == 0) {
        Py_Initialize();
    }

    // make sure the GIL is correctly initialized
    if (PyEval_ThreadsInitialized() == 0) {
        PyEval_InitThreads();
    }

    Py_InitModule("Foo", ModuleMethods);

    PyEval_ReleaseThread(PyGILState_GetThisThreadState());
    fprintf(stdout, "Python environment initialized\n");
}