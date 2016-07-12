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

The following are tests I most likely broke during the move. Most of these are issues with `mock.patch` not set up correctly for the new structure 

`test_pdconfd:336`: raises OSError trying to write to `/etc/config`

`test_main:4`: the patch decorator screwed up due to module name changes

`test_exc`: whole thing

`test_lib_config:112`: patch fail

`test_fc:42`: patch fail

`confd/test_{resource, traffic, runtime, name, files}`: patch and migration issues

`confd/test_manager:116`: OSError on `/etc`

`chute/test_updateObject`: patches updateObject.exc, but the plan content from exc was moved to chute. I updated the patch with no progress.

`chute/test_restart:29`: patch failure









































