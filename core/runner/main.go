package main

// Entry point into core and rest of paradrop system

func checkError(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	end := make(chan bool)

	for i := 0; i < 1; i++ {
		go create_thread(i)
	}

	<-end
}
