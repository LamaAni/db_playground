# Experiment design

1. Requirements and goals
1. Data structure and API's
1. Design
1. Discussion

## Requirements and Goals

### Goals of the logger

1. A logical clock based log.
1. Allows writing data entities to disk.
1. Includes write modes,
   - Fast, in memory. May lose data.
   - Slow, direct to disk. Data is persistent.

### Functional Requirements

1. Keeps a recoverable copy of the logical clock on disk.
1. Can seek fast.
1. Has read cursors
   - Cursors can store current location to disk.
   - Cursor can seek, as fast as possible. (Index?)
1. Can replay from any point in the cursor, in the case of recovery.
1. Log is split into files, each file, starts its own logical clock.
1. Logrotate can be executed.
1. Includes persistence modes,
   - In memory: entry is stored to memory and lazily to disk
     - periodic flush
     - buffer flush
   - Disk sync: entry is given a disk persistence and call will not complete until disk writing is done.

### Non Functional requirements

1. The data should be stored in a log file that can be rotated. From logrotate use the mode `copytruncate`- Truncate the original log file in place after creating a copy, instead of moving the old log file and optionally creating a new one.
1. Signal machine.
1. Persistent multi location storage? Optional - avoid disk corruption, but maybe slower?

## Data structures and API's

Entry,

- ls: logical clock entry
- ts: timestamp
- data: binary
- hash: data hash

### API's

For the web api, this is an optional thing. So I think we should not add it. We can in general create the package and allow api calls to be made via an vertically mounted service in code.

Otherwise the interaction api is just in code, including,

1. logging methods
1. decorators - automatically apply all methods as decorators to allow recovery of the calls in the case of bad processing. The call will be marked as complete once the method ends (ack)

## High level design
