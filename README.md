# Paradrop

Version 2-- no pex, snappy-remote, vagrant, or kvm. Or twisted, if I have my way! These are instructions for working on Paradrop, not making chutes. 

## Setup

Install the dev tools. Paradrop is built as a snap using `snapcraft`.

```
$ sudo add-apt-repository ppa:snappy-dev/tools
$ sudo apt-get update
$ sudo apt-get install snapcraft ubuntu-device-flash
```

There are a number of ways to build and run Paradrop, one of which involves directly invoking `go`. If you want to go this route (which is likely the fastest way to develop) you'll need to have go installed. See the instructions (here)[https://golang.org/doc/install]. 

### Building Paradrop

When it comes to running the paradrop service, you've got options. Here they are in order of speed. 

#### Directly  

Execute the go script directly. You must have go, python 2.7, pip, and the python development tools installed. 

```
# Make sure go is installed
go version #=> go version go1.6 linux/amd64

# grab the python headers
sudo apt-get install python-dev
```

The go core essentially runs `import paradrop`, so you have three choices on how to satisfy that import.

Installing to system (quick): 

```
sudo pip install -e python
```

Installing to virtualenv (safe): 

```
virtualenv env
source env/bin/activate
pip install -e python
```

Temporarily updating PYTHONPATH (best):

```
export PYTHONPATH=python
```

Pull the trigger on one of these then start paradrop with:

```
go run core/*.go
```

### Staged

Snaps are a lot like docker containers in that they wrap up a progam and all dependencies. Snapcraft has an intermediate build option that allows you to run your program in a production-like environment. 

You do not need go or python installed. 

```
$ snapcraft stage # builds project within parts/ directory
$ snapcraft shell # drop into environment
snapcraft: $ core # directly start the core 
```

### Containerized

Run the project within a containerized snappy on your host operating system. 

```
# build the snap
snapcraft assemble

# run the snap
snapcraft run  
```

This downloads an ubuntu container and launches the snap within it. Be warned that the container cant do much in terms of networking. You'll need to pass arguments along to `kvm` to set up forwarding before calling `snapcraft run` to forward container ports to host ports.

```
export SNAPCRAFT_RUN_QEMU_ARGS="-redir tcp:7979::7979"
```

The arguments are not limited to networking: 

```
export SNAPCRAFT_RUN_QEMU_ARGS="-usb -device usb-host,hostbus=1,hostaddr=10"
```


### Virtualized

Like containerized, but runs snappy in a virtual machine instead of a container. Head to (the snappy website)[https://developer.ubuntu.com/en/snappy/start/], download your favorite VM image, and then upload your snap.

```
snapcraft assemble
snappy-remote install -url ubuntu@localhost *.snap
```

Note: command not verified. More detail to follow

### Flashed

Flash paradrop onto a physical device. 

Instructions to follow. 

## Working with Snapcraft

See tutorial on [making your first snap](https://github.com/snapcore/snapcraft/blob/master/docs/your-first-snap.md) with snapcraft. Their github also has a nice set of [demo applications](https://github.com/snapcore/snapcraft/tree/master/demos).

Not sure whats going on? Check out `snapcraft help sources` and `snapcraft help plugins` for documentation on config file structure.

## Managing Snappy

Get logs from a running service: 
```
sudo snappy service logs ethereum
```

Start, stop, or restart services: 

```
# with a service called "ethereum"

sudo snappy service start ethereum
sudo snappy service stop ethereum
sudo snappy service restart ethereum
```

See [this link](https://blog.slock.it/let-s-play-with-snappy-ethereum-816588198528#.bwel1tmb1) for more info.

### Updating

We may be able to let snaps update themselves.See `snapd-control` [here](https://developer.ubuntu.com/en/snappy/guides/interfaces/).

### Running Tests

Paradrop uses `nose` to test the python code. From the root directory: 

```
nosetests
```

Make sure you have nose installed: 

```
pip install nose
```

# Scratch

Random notes follow.

Information on installing python packages as part of the yaml file: https://gist.github.com/ericoporto/87996bef1bf492e2fabf161ea7219994

To run directly: 

```
export PYTHONPATH=paradrop/docker
go run core/main.go
```

## Random TODO

- Convert nexus and settings into a conf file that the core reads
- Migrate settings to the core
- Set up webserver
- Pass argslist onto python from go 
- Deal with multiple `pthread`s accessing the python modules
- Integrate pdtools

See here for the 2.7 problem: https://github.com/docker/docker-py/issues/1019
