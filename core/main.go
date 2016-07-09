package main

// Simple starter script to kick off the go core

import "github.com/damouse/gosnake"

func main() {
	// fmt.Println("Go: Starting Paradrop")

	pymodule := gosnake.NewBinding()
	pymodule.Import("paradrop")
	pymodule.Call("paradrop", "main", "callme")
}
