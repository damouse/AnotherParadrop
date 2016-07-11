# Refactor Log

This is a list of refactor changes. 

Last commit before the directory fork:

```
commit 1e21a15d22fa8122ba76091ab499a4bd8d4f9f5b
Author: Lance Hartung <lance@paradrop.io>
Date:   Fri Jul 8 13:20:51 2016 -0500

    Added unit tests for new code.

```

## File Merges

#### backend.exc: 

Old: (backend.exc.) files, name, plans resource, runtime, state, struct, traffic

New: backend.exec.plans

Updated: fc.updateObject 

#### lib.api: 

pdrest -> pdapi
Updated: (pdfcd.) server, apichute`

#### lib.utils: 

pdosq -> pdos
Functions: pdosq.makedirs -> pdos.makedirs_quiet
Updated: lib.utils.uci, pdconfd.config.wireless, manager

`lib.utils.pdinstall` -> `backend.apiinternal`

#### lib.utils

storage -> backend.fc.chutestorage

## Directory Migrations

`pdtools`, `pdtools.lib` -> `paradrop.shared`

`lib.config` -> `config`

`backend.pdconfd` -> `confd`

`backend.exc`, `backend.fc` -> `chute`

`backend.pdfcd` -> `backend`

`lib.chute` -> `chute.chute`

`lib.utils.dockerapi` -> `chute.dockerapi`

`lib.utils.restart` -> `chute.restart`

`lib.utils.uci` -> `config.uci`

## Deleted

`lib.utils.addresses`: unused

## Directory Update Notes

Notes on the original structure:

- backend
    + exc: chute updating and plans
        * executionplan: make and run plans that update chutes
        * plangraph:  Plan and PlanMap objects
        * plans: actual steps
    + fc: chute configuration, interface into exec
        * chutestorage: ChuteStorage(pd.lib.utils.storage)
            - Nothing else implements storage
        * configurer: in charge of chute config changes
            - Only used by backend.pdfcd.server
        * updateObject: UpdateObject and UpdateChute. top level exc api object
            - Used by fc.configurer
    + pdconfd
        * config: doesnt need lots of changes
            - base: ConfigObject base class. Used all over pdconfd
            - command: Command, CommandList, KillCommand
            - dhcp: ConfigDHCP, ConfigDnsmaq. Dont look used (?)
            - firewall: ConfigRedirect, ConfigZone
            - manager: loads all config subclasses
            - network
            - wireless
        * client: client for config changes
        * main: entry point into pdconfd
    + pdfcd
        * apibridge: bridges http api to wamp
        * apichute: chute HTTP api call implementation
            - create, delete, stop, start
        * apiinternal: wamp api
            - ping, update, getConfig, setConfig, createChute, deleteChute, startChute, stopChute, logs
            - Base exposes XMLRPC functions, used in pdfcd.server
        * apiutils: redundant api helper methods
        * server: core server implementation
            - Twisted/threading implementation for everything else
- lib
    + api
        * pdapi: rest server indirection and over-the-top util methods
    + config
        * configservice: one function, pokes the client
        * devices: detects system devices/capabilities
        * dhcp: dhcp config
        * dockerconfig: one function, translates representation and turns it to chutes
        * firewall
        * hostconfig: top level module (ish?) that generates host config repr
        * network
        * osconfig: one function
        * pool: network pool resource management
        * uciutils: utility functions for managing uci options
        * wifi: wireless config
    + utils
        * addresses: random networking utils
        * dockerapi: interface into docker
        * pdos: kinda weird wrappers around os functions
            - Implements read/write file functions
        * restart: device restart handling. communicates with pdconfd
        * uci: wrapper around uci config
    + chute: 5 constants Only used in chutestorage and updateobject
    + pdinstall: triggers pdinstall to update pd
    + settings: global settings storage
- localweb: I do not belong in the paradrop root directory.
- pdtools
    + lib
        * cxbr: autobahn wrapper
        * names: dot namespace implementation. Remove.
        * nexus: global config object
        * output: wildly overengineered logging service
        * pdutils: random utility functions
        * store: yet another persistence implementation

Proposed directory structure: 

- backend
    + pdfcd.server
    + pdfcd.internal (is this still needed?)
    + lib.api
- chute
    + executionplan
    + plangraph
    + plans
    + chutestorage (temp)
    + configurer
    + updateObject
    + lib.chute
- confd
    + client
    + main
    + configobjects (all of them)
- config
    + lib.config.configservice (?)
    + lib.config.devices
    + lib.config.dockerconfig
    + lib.config.osconfig
    + lib.utils.dockerapi
    + lib.utils.pdos
    + lib.utils.restart
    + lib.pdinstall
    + lib.config.dhcp
    + lib.config.firewall
    + lib.config.hostconfig (?)
    + lib.config.network
    + lib.config.pool
    + lib.config.uciutils
    + lib.config.wifi
    + lib.utils.uci
- localserver
    + lib.utils.addresses
    + pdfcd.apuchute
- shared
    + pdfcd.apiutils
    + lib.settings
    + shared.store
    + shared.output
    + shared.nexus
    + backend.fc.chutestorage

Orphaned: 

- apibridge
- apichute























































