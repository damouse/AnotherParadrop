package main

/*
#cgo pkg-config: python-2.7
#include "Python.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>

extern PyObject* callback(PyObject* arg);

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
    {NULL},
};

static void initialize_python () {

    if (Py_IsInitialized() == 0) {
        Py_Initialize();
        // fprintf(stdout, "> Py_Initialize\n");
    }

    // make sure the GIL is correctly initialized
    if (PyEval_ThreadsInitialized() == 0) {
        PyEval_InitThreads();
        // fprintf(stdout, "> PyEval_ThreadsInitialized\n");
    }

    PyObject *module = Py_InitModule("Foo", ModuleMethods);

    PyEval_ReleaseThread(PyGILState_GetThisThreadState());
}
*/
import "C"

import (
	"fmt"
	"sync"
	"unsafe"

	"github.com/sbinet/go-python"
	"github.com/spikeekips/go-pthreads"
)

func init() {
	C.initialize_python()
}

//export callback
func callback(args *C.PyObject) *C.PyObject {
	a := python.PyObject_FromVoidPtr(unsafe.Pointer(args))
	iter := python.PySeqIter_New(a)

	converted := []interface{}{}

	for i := 0; i < python.PyTuple_Size(iter); i++ {
		p := python.PyTuple_GetItem(iter, i)
		s := python.PyString_AsString(p)
		converted = append(converted, s)
	}

	fmt.Printf("Go code called!: %s\n", converted)

	return nil
}

func checkError(e error) {
	if e != nil {
		panic(e)
	}
}

func embed_function(num int) {
	_module := python.PyImport_ImportModuleNoBlock("json_dump")

	// get the function
	_attr := _module.GetAttrString("run")

	// pack arguments
	a := python.PyTuple_New(1)
	python.PyTuple_SET_ITEM(a, 0, python.PyInt_FromLong(num))

	_result := _attr.CallObject(a)
	r := python.PyString_AsString(_result)

	fmt.Println("GO: ", r)
}

var lock sync.Mutex

func create_thread(num int) {
	lock.Lock()
	defer lock.Unlock()
	done := make(chan bool)

	thread := pthread.Create(func() {
		gil := C.PyGILState_Ensure()
		defer C.PyGILState_Release(gil)

		embed_function(num)
		done <- true
	})

	defer thread.Kill()
	<-done
	close(done)
}

func main() {
	end := make(chan bool)

	for i := 0; i < 1; i++ {
		go create_thread(i)
	}

	<-end
}

// func main() {
//     fmt.Println("Starting up!")
//     panic(http.ListenAndServe(":7987", http.FileServer(http.Dir(".."))))
// }
