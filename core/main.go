package main

/*
#cgo pkg-config: python-2.7
#include "Python.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>

extern PyObject* callback(PyObject* arg);
extern PyObject* port(PyObject *self, PyObject *args);

#define _gopy_max_varargs 8

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
        fprintf(stdout, "> Py_Initialize\n");
    }

    // make sure the GIL is correctly initialized
    if (PyEval_ThreadsInitialized() == 0) {
        PyEval_InitThreads();
        fprintf(stdout, "> PyEval_ThreadsInitialized\n");
    }

    PyObject *module = Py_InitModule("Foo", ModuleMethods);

    PyEval_ReleaseThread(PyGILState_GetThisThreadState());
}
*/
import "C"

// Steps to expose a method to python:
//  1) Add a new declaration to the list of externs at the top of the C code above
//  2) Implement the method, taking 2 pyobjects and returning 1
//  3) Write "//export NAME" above the method in Go
//  4) Add a new line to ModuleMethods in the C code above. Check thet other entries

import (
	"fmt"
	"sync"
	"unsafe"

	"github.com/sbinet/go-python"
	"github.com/spikeekips/go-pthreads"
)

var lock sync.Mutex

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

//export port
func port(self *C.PyObject, args *C.PyObject) *C.PyObject {
	fmt.Println("GO: public exported called")
	return nil
}

func embed_function(num int) {
	_module := python.PyImport_ImportModuleNoBlock("paradrop")
	fmt.Println("Havve", _module)

	// get the function
	// _attr := _module.GetAttrString("run")

	// // pack arguments
	// a := python.PyTuple_New(1)
	// python.PyTuple_SET_ITEM(a, 0, python.PyInt_FromLong(num))

	// _result := _attr.CallObject(a)
	// r := python.PyString_AsString(_result)

	// fmt.Println("GO: ", r)
}

func testFunctionTypes(name string, age int) {
	_module := python.PyImport_ImportModuleNoBlock("paradrop")
	attr := _module.GetAttrString("main")

	// main := attr.GetAttrString("main")

	fmt.Println("Havve", attr.Check_Callable())

	// attr := _module.GetAttrString("talk")

	// a := python.PyTuple_New(2)
	// python.PyTuple_SET_ITEM(a, 0, python.PyString_FromString(name))
	// python.PyTuple_SET_ITEM(a, 1, python.PyInt_FromLong(age))

	ret := attr.CallObject(python.PyTuple_New(0))

	// Python threw an exception!
	if ret == nil {
		python.PyErr_PrintEx(false)
	}

	fmt.Println("GO: Done", ret)
}

// // pyfmt returns the python format string for a given go value
func pyfmt(v interface{}) (unsafe.Pointer, string) {
	switch v := v.(type) {
	case bool:
		return unsafe.Pointer(&v), "b"

		//  case byte:
		//      return unsafe.Pointer(&v), "b"

	case int8:
		return unsafe.Pointer(&v), "b"

	case int16:
		return unsafe.Pointer(&v), "h"

	case int32:
		return unsafe.Pointer(&v), "i"

	case int64:
		return unsafe.Pointer(&v), "k"

	case int:
		switch unsafe.Sizeof(int(0)) {
		case 4:
			return unsafe.Pointer(&v), "i"
		case 8:
			return unsafe.Pointer(&v), "k"
		}

	case uint8:
		return unsafe.Pointer(&v), "B"

	case uint16:
		return unsafe.Pointer(&v), "H"

	case uint32:
		return unsafe.Pointer(&v), "I"

	case uint64:
		return unsafe.Pointer(&v), "K"

	case uint:
		switch unsafe.Sizeof(uint(0)) {
		case 4:
			return unsafe.Pointer(&v), "I"
		case 8:
			return unsafe.Pointer(&v), "K"
		}

	case float32:
		return unsafe.Pointer(&v), "f"

	case float64:
		return unsafe.Pointer(&v), "d"

	case complex64:
		return unsafe.Pointer(&v), "D"

	case complex128:
		return unsafe.Pointer(&v), "D"

	case string:
		cstr := C.CString(v)
		return unsafe.Pointer(cstr), "s"

	case *python.PyObject:
		return unsafe.Pointer(topy(v)), "O"

	}

	panic(fmt.Errorf("python: unknown type (%v)", v))
}

func topy(self *python.PyObject) *C.PyObject {
	return (*C.PyObject)(unsafe.Pointer(self))
}

func togo(obj *C.PyObject) *python.PyObject {
	if obj == nil {
		return nil
	}

	return python.PyObject_FromVoidPtr(unsafe.Pointer(obj))
}

func create_thread(num int) {
	lock.Lock()
	defer lock.Unlock()
	done := make(chan bool)

	thread := pthread.Create(func() {
		gil := C.PyGILState_Ensure()
		defer C.PyGILState_Release(gil)

		testFunctionTypes("joe", num)

		done <- true
	})

	defer thread.Kill()
	<-done
	close(done)
}

func checkError(e error) {
	if e != nil {
		panic(e)
	}
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
