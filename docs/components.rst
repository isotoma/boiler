Components
==========

Yaybu Server is primarily a set of loosely coupled components that can be
integrated to suit your particular needs rather than a monolithic one-purpose
system.


Tasks
-----

Actions performed by Yaybu Server are modelled as a Task. The act of
deploying with Yaybu is seperated from the Task management code to
allow other tasks to be orchestrated by Yaybu.

See Task, CompondTask, Tasks


Deployment Task
---------------

There is an implementation of the Task API that can deploy to a server using
Yaybu.


Triggers
--------

Triggers are responsible for actually calling addTask and triggering work.


