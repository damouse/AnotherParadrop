# Paradrop

## Getting Started 

These are instructions for working on Paradrop, not making chutes. 

### Installing Dev Tools

You'll need to have Go installed. Instructions coming.

Install vagrant:

```
sudo apt-get install virtualbox vagrant snapcraft
vagrant init http://cloud-images.ubuntu.com/snappy/15.04/core/stable/current/core-stable-amd64-vagrant.box
```

### Interacting with Dev Environment

Start up the virtual machine: 

```
vagrant up
```

Connect to a running VM: 

```
vagrant ssh
```

The username and password are both `ubuntu`.


### Creating Snaps

See tutorial on [making your first snap](https://github.com/snapcore/snapcraft/blob/master/docs/your-first-snap.md) with snapcraft. Their github also has a nice set of [demo applications](https://github.com/snapcore/snapcraft/tree/master/demos).

Download these with:

```
git clone https://github.com/snapcore/snapcraft
cd snapcraft/demos
```

Create a new snap: 

```
snapcraft init
```

Stage the project:

```
snapcraft stage
```

Build the snap: 

```
snapcraft assemble
```

Run the snap. Note that I haven't been able to get this to work yet.

```
snapcraft run
```

Not sure whats going on? Check out `snapcraft help sources` and `snapcraft help plugins` for documentation on config file structure.

# Scratch

Random notes.

It seems `snapcraft run` starts the snap in a linux container.

```
$ sudo add-apt-repository ppa:snappy-dev/tools
$ sudo apt-get update
$ sudo apt-get install snapcraft ubuntu-device-flash
```

snapcraft ubuntu-device-flash ubuntu-snappy-cli