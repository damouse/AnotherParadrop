package main

// Simple starter script to kick off the go core

func main() {
	end := make(chan bool)

	for i := 0; i < 1; i++ {
		go Create_thread(i)
	}

	<-end
}
