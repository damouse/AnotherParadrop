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

#### lib.utils

storage -> backend.fc.chutestorage

## Directory Updates

`pdtools` moved to paradrop.pdtools

Deleted pdtools.coms 

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

Redundant Settings/Storage:
- backend.fc.chuteshorage

#### Existing Structure Notes

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

























































