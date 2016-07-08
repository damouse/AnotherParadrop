# Paradrop

Version 2-- no pex, snappy-remote, vagrant, or kvm. Or twisted, if I have my way! These are instructions for working on Paradrop, not making chutes. 

## Building Paradrop

Install the dev tools. Paradrop is built as a snap using `snapcraft`.

```
$ sudo add-apt-repository ppa:snappy-dev/tools
$ sudo apt-get update
$ sudo apt-get install snapcraft ubuntu-device-flash
```

Once installed, go ahead and build paradrop:

```
snapcraft stage
```

This will download all dependencies, compile all the necesary components, and put them all in `stage`. You can execute paradrop directly from here!

To build the snap: 

```
snapcraft assemble
```

Finally, to run the snap:

```
snapcraft run
```

You can also execute the binary directly:

```
# note: name may be different
stage/bin/core
```

As well as drop into a `snapcraft shell`, where you have access to the full environment as if you were installed: python packages, go, etc.

```
$ snapcraft shell
$ snapcraft: core
```

This downloads an ubuntu container and launches the snap within it. Be warned that the container cant do much in terms of networking. You'll need to pass arguments along to `kvm` to set up forwarding.  

```
export SNAPCRAFT_RUN_QEMU_ARGS="-redir tcp:7979::7979"
```

The arguments are not limited to networking: 

```
export SNAPCRAFT_RUN_QEMU_ARGS="-usb -device usb-host,hostbus=1,hostaddr=10"
```

### Help with Snapcraft

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

# Scratch

Random notes follow.

Information on installing python packages as part of the yaml file: https://gist.github.com/ericoporto/87996bef1bf492e2fabf161ea7219994
