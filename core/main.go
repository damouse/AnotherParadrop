package main

import (
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("Starting up!")
	panic(http.ListenAndServe(":7987", http.FileServer(http.Dir(".."))))
}
