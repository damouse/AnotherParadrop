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

#### lib.utils.storage -> backend.fc.chutestorage


## Directory Updates

Notes on the original structure:

- backend
    + exec: chute updating and plans
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


#### Proposed

- Merge backend.exc and backend.fc
- backend.exc + backend.fc > chutes
- pdconfd > networkconfig
    + Package not dependant on any other paradrop files except for `manager` 
- pdfcd.apiutils > lib.utils.network
- lib.config: wifi, osconfig, dockerconfig, configservice
    + Are all of these used exclusively by pdconfd?
- lib.utils
    + dockerapi doesnt belong here
    + pdosq needs a new home
    + Restart: needs a new home
- pdtools.lib
    + remove cxbr, names
- pdfcd
    + pdfcd.server.initializeSystem is only used in one place and in one test

Redundant Settings/Storage:
- backend.fc.chuteshorage

Would it really be so bad to replace the million log, settings, and chute file systems and manipulators with a database inside the snap? 






















































