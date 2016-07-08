package main

// Conversion between C.Python and python.PyObject types to and from G

/*
#cgo pkg-config: python-2.7
#include "Python.h"
*/
import "C"

import (
	"fmt"
	"unsafe"

	"github.com/sbinet/go-python"
)

// pyfmt returns the python format string for a given go value
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