package main

// Simple starter script to kick off the go core

func main() {
	// Init python environment
	InitPyEnv()

	// Start the server
	end := make(chan bool)

	// os.Args

	for i := 0; i < 1; i++ {
		go Create_thread(i)
	}

	<-end

	// Run forever
}
