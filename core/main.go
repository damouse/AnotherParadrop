package main

import (
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("Starting up!")
	panic(http.ListenAndServe(":8080", http.FileServer(http.Dir("."))))
}
