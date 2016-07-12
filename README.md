# Paradrop

Version 2-- no pex, snappy-remote, vagrant, or kvm. Or twisted, if I have my way! These are instructions for working on Paradrop, not making chutes. 

## Setup

Install the dev tools. Paradrop is built as a snap using `snapcraft`.

```
$ sudo add-apt-repository ppa:snappy-dev/tools
$ sudo apt-get update
$ sudo apt-get install snapcraft ubuntu-device-flash
```

### Building Paradrop

When it comes to running the paradrop service, you've got options. Here they are in order of speed. 

Directly run paradrop as a python program:  

```
pip install -e src/requirements.txt
export PYTHONPATH=src
python -m paradrop.main --local
```

#### Staged

Let snapcraft download dependencies and build the environment, then run paradrop in that environment.

```
$ snapcraft stage  # builds project within parts/ directory
$ snapcraft shell  # drop into environment
snapcraft: $ paradrop --local
```

#### Containerized

Run the project within a containerized snappy on your host operating system. 

```
snapcraft assemble
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


*NOTE*: as of this writing `snapcraft run` always fails when `frameworks: docker` is listed in the yaml. The run command never suceeds, but you cant ssh in to install docker until it does. You have to manually boot the image and install docker. 

Snapcraft will download the image for you after running `snapcraft run` the first time. After doing do:

```
# Boot the image
kvm -m 512 -netdev user,id=net0,hostfwd=tcp::8090-:80,hostfwd=tcp::8022-:22,hostfwd=tcp::9999-:14321,hostfwd=tcp::9000-:9000 -netdev user,id=net1 -device e1000,netdev=net0 -device e1000,netdev=net1 $WIFI_CMD image/15.04.img

# Connect to it
ssh -p 8022 ubuntu@localhost
```

Username/password are both `ubuntu` by default.

#### Virtualized

*NOTE: steps not verified-- YMMV*

Like containerized, but runs snappy in a virtual machine instead of a container. Head to [the snappy website](https://developer.ubuntu.com/en/snappy/start/), download your favorite VM image, and then upload your snap.

```
snapcraft assemble
snappy-remote install -url ubuntu@localhost *.snap
```

#### Flashed

Flash paradrop onto a physical device. 

Instructions to follow. 


## Working with Snapcraft

See tutorial on [making your first snap](https://github.com/snapcore/snapcraft/blob/master/docs/your-first-snap.md) with snapcraft. Their github also has a nice set of [demo applications](https://github.com/snapcore/snapcraft/tree/master/demos).

Especially useful is the [snapcraft.yaml syntax page](https://developer.ubuntu.com/en/snappy/build-apps/snapcraft-syntax/).

Not sure whats going on? Check out `snapcraft help sources` and `snapcraft help plugins` for documentation on config file structure.

## Managing Snappy

Get logs from a running service: 
```
sudo snappy service logs paradrop
```

Start, stop, or restart services: 

```
# with a service called "paradrop"

sudo snappy service start paradrop
sudo snappy service stop paradrop
sudo snappy service restart paradrop
```

See [this link](https://blog.slock.it/let-s-play-with-snappy-ethereum-816588198528#.bwel1tmb1) for more info.

### Updating

We may be able to let snaps update themselves. The permission is called [snapd-control](https://developer.ubuntu.com/en/snappy/guides/interfaces/). Also useful: the [snapd wiki page](https://github.com/intelsdi-x/snap/blob/master/docs/SNAPD.md).

### Running Tests

Paradrop uses `nose` to test the python code. From the root directory: 

```
nosetests
```

Make sure you have nose installed: 

```
pip install nose
```

## Interacting with Snappy

See the wiki page [on debugging snaps](https://developer.ubuntu.com/en/snappy/build-apps/debug/)

## Scratch

Random notes follow.

Information on installing python packages as part of the yaml file: https://gist.github.com/ericoporto/87996bef1bf492e2fabf161ea7219994

To run directly: 

```
export PYTHONPATH=paradrop/docker
go run core/main.go
```

### Additional Binaries

These are notes @damouse wrote while re-adding binaries for the snapcraft migration. 

Added `hostapd` and `dnsmasq` to `snapcraft.yaml`. When running `snapcraft stage` they appear in the staging directory, but I suspect they're not making it to the final snap. Need to verify they get copied over, that paradrop can access them, and that they have the neccesary permissions.

Added `frameworks: docker` and `caps: docker_client`. This does not automatically install the docker snap, unfortunatly. 

Havent converted the snap from an app to a framework. Likely will have to, but haven't hit anything that failed majorly yet to need it. 

Pipework should be copied over-- but does it copy over to the root directory that snappy calls `start` on our service? Make sure that the script shows up in the right place and is callable.

No progress on auto-updating.

Snapcraft just assembles snaps (still very useful!) in the `snap/` directory, it doesn't fundementally change their structure. If any of these steps cause us problems we can override the final product before snapping it ourselves.


### Scratch

Random notes.

Copying the snap manually:

```
scp -i /home/damouse/.ssh/id_rsa -oStrictHostKeyChecking=no -oUserKnownHostsFile=/tmp/tmpx_dx6dgk -oKbdInteractiveAuthentication=no -P 8022 /home/damouse/code/python/paradrop/paradrop_3_amd64.snap ubuntu@localhost:~/
```
