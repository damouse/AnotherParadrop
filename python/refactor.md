# Refactor Log

This is a list of refactor changes. 

Last commit before the directory fork:

```
commit 1e21a15d22fa8122ba76091ab499a4bd8d4f9f5b
Author: Lance Hartung <lance@paradrop.io>
Date:   Fri Jul 8 13:20:51 2016 -0500

    Added unit tests for new code.

```

## Directories

- `pdtools` is now under paradrop/pdtools. References in whole project updated

## Files

Each entry here lists the name of the pacakges changed, the changes, and any side-effect updates.

#### backend.exc: 

Old: (backend.exc.) files, name, plans resource, runtime, state, struct, traffic

New: backend.exec.plans

Updated: fc.updateObject 

#### lib.api: 

pdrest -> pdapi
Updated: (pdfcd.) server, apichute`



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

Redundant Settings/Storage:
- backend.fc.chuteshorage