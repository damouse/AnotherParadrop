package main

// Simple starter script to kick off the go core

import (
	"os"
	"strings"

	"github.com/damouse/gosnake"
)

func main() {
	args := strings.Join(os.Args[1:], " ")

	pymodule := gosnake.NewBinding()
	pymodule.Import("paradrop")
	pymodule.Call("paradrop", "main", args)
}
