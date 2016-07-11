package main

import (
	"os"
	"strings"

	"github.com/damouse/gosnake"
)

func main() {
	// Import the paradrop module and call main on it

	args := strings.Join(os.Args[1:], " ")

	module, _ := gosnake.Import("paradrop")

	module.Call("main", args)
}
