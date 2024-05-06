# Experiment design

1. Requirements and goals
1. Data structure and Entities
1. Design
1. Discussion

## Requirements and Goals

### Goals of the logger

1. A logical clock based log.
1. Allows writing data entities to disk.
1. Includes write modes,
   - Fast, in memory. May lose data.
   - Slow, direct to disk. Data is persistent.

### Requirements

1. Keeps a recoverable copy of the logical clock on disk.
1. Can seek fast.
1. Has read cursors
   - Cursors can store current location to disk.
   - Cursor can seek, as fast as possible.
1. Log is split into files, each file, starts its own logical clock.
1. Logrotate can be executed.
