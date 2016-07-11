# Design

This document lays out the design for server api, router api, and their communication. Models are included for completeness. 

Definitions: 

- *pdlabs*: the developers of paradrop and pdserver
- *router*: the paradrop service (virtualized or physical)
- *server*: our backend
- *user*: is the owner of a router
- *identity*: unique name and secret authentication information 

## Requirements

#### Routers...

Belong to a user

Get their identity manually from a user

Can communicate with server iff they have identity

Configurable via server and local HTTP API

Update themselves without local (SSH) access 

Store, install, remove, and configure chutes

Provide metadata about performance and statistics to users

Log all events

Provide logs to users and pdlabs

Configure local networking functionality

### Users...

Can access the router direct
