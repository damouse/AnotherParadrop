package main

// Simple starter script to kick off the go core

import (
	"os"
	"strings"

	"github.com/damouse/gosnake"
)

func main() {
	args := strings.Join(os.Args[1:], " ")

	module, _ := gosnake.Import("paradrop")

	module.Call("main", args)
}
