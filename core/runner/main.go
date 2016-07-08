package main

// Simple starter script to kick off the go core

import paradrop ".."

func main() {
	end := make(chan bool)

	for i := 0; i < 1; i++ {
		go paradrop.Create_thread(i)
	}

	<-end
}
