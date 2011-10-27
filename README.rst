Yaybu Server
============

This package contains a simple twisted daemon for orchestrating actions against
multiple servers with Yabu.

There are 2 ways to set up a development environment. You can use buildout::

    $ python bootstrap.py
    $ bin/buildout

A ``boiler`` and ``boil`` script will be created in the bin/ directory.

You can also use virtualenv::

    $ virtualenv boiler
    $ source boiler/bin/active
    $ python setup.py develop


To run a server in foreground::

    $ boiler -c boiler-sample start -n

``boiler-sample`` is a Yay file in the root of the repository that contains a
description of which services and triggers to start with the main Boiler
service. It looks something like this::

    services:
      - PbService:
          port: 8787
      - WebService:
          port: 8080


To execute a task::

    $ boil << HERE
    tasks:
      - Yaybu:
          name: deploy-application
          host: jolt
    HERE

