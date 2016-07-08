package main

// Bindings between go and python

/*
#cgo pkg-config: python-2.7
#include "Python.h"
#include "proxy.h"
*/
import "C"

import (
	"fmt"
	"sync"
	"unsafe"

	"github.com/sbinet/go-python"
	"github.com/spikeekips/go-pthreads"
)

// Steps to expose a method to python:
//  1) Add a new declaration to the list of externs at the top of the C code above
//  2) Implement the method, taking 2 pyobjects and returning 1
//  3) Write "//export NAME" above the method in Go
//  4) Add a new line to ModuleMethods in the C code above. Check thet other entries

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

// An example of publically exposing a method to python
//export port
func port(self *C.PyObject, args *C.PyObject) *C.PyObject {
	fmt.Println("GO: public exported called")
	return nil
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
