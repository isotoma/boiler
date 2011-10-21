Yaybu Server
============

This package contains a simple twisted daemon for orchestrating actions against
multiple servers with Yabu.

To run a server::

    $ boiler -n start

To execute a task::

    $ boil << HERE
    tasks:
      - Yaybu:
          name: deploy-application
          host: jolt
    HERE

