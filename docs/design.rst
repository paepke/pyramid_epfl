EPFL design decisions
=====================

Server side state
-----------------

In webapplications there are many ways to transport data between client and server. Picking between the different
containers, transport methods, request methods is unnecessary in case of most business applications. The same holds true
for temporarily persisting data.

Server side state is the EPFL choice to achieve the following:
1. Communication between client and server is standardized and done by EPFL.
2. All data is stored server side.
3. All data is manipulated server side.
4. All data manipulation is done in python.

Thus business logic is centralized in one place. Easy to use and convenient to access and change by the developer.


Self rendering trees
--------------------

While there are numerous ways to structure a website, the default use case in business applications itself follows a
mostly strict tree structure. Activities have tasks, tasks have sub tasks and so on.

EPFL supports this by exploiting the self rendering capabilities of its components in order to automatically generate
even the most complex of structures and keeping them up to date.

The task of a developer using EPFL is to provide the general structure of Components, handle events and manipulate data,
while EPFL and its Components deal with showing the results and providing the interface to the user.

EPFL provides you with:
 - Builtin pagination
 - Builtin search
 - Components for every purpose, be it...
    ... showing pretty graphs

    ... listing data

    ... manipulating lists

    ... editing data

    ... and many more


Dynamic extension of classes
----------------------------

If you toyed around with the examples you will have noticed the somewhat strange notation EPFL uses to define a pages
structure. The reason behind this is a simple principle: *Every Component can be used to seamlessly create slightly
altered copies of itself.* You can provide values for new attributes, you can provide new functions, you can even change
default values of attributes up to and including functions to whatever you desire.

At the core of this lies the :class:`solute.epfl.core.epflcomponentbase.UnboundComponent` and its twin brother, albeit
non-identical, :class:`solute.epfl.core.epflcomponentbase.ComponentBase`.

Inside the EPFL core those UnboundComponents are converted just in time into ComponentBase instances. The first being
used to define structures and persist data, the latter being used in the lifecycle driven request-flow of
:class:`solute.epfl.core.epflpage.Page`.

This allows the developer to create abstractions of base classes, allowing him to change the way a Component works
dramatically. All with little to no effort and without making complex jumps of thought through multiple layers of code.
