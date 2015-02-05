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

Model View Controller
---------------------
Everyone and everyone's cat uses MVC nowadays. MVC is to frameworks what "agile" is to process management, meaning
everyone has his own personal definition and uses it accordingly.

There are two layers in EPFL that use the MVC scheme:
 - Globally in :class:`~solute.epfl.core.epflpage.Page` there's :attr:`~solute.epfl.core.epflpage.Page.model`
   wherein a :class:`~solute.epfl.core.epflassets.ModelBase` class is stored and instantiated every request. From the
   perspective of a developer using EPFL the page acts primarily as model and view, while internally it takes the role
   of a central controller as well.
 - Locally in :class:`~solute.epfl.core.epflcomponentbase.ComponentBase` there's
   :attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.compo_state` that gives you the ability to use any component
   as its own model by setting up attributes to be stored in the transaction. Going by the concept your controllers are
   event handles and the life cycle methods
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.after_event_handling`,
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.compo_destruct`,
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.finalize`,
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction`,
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.pre_render`,
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.setup_component` and finally
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.setup_component_state` for
   :class:`~solute.epfl.core.epflcomponentbase.ComponentBase` and the method
   :meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_struct` for
   :class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase`. Event handles are defined by writing methods
   with the prefix handle\_ that are called when events are sent via ajax.

In order to take full advantage of EPFLs automatic features (like the get_data pattern you see in the
:doc:`users/tutorial/index`) it is highly recommended to keep those separated as much as possible. If you are in a local
controller and want to store data that is not meant to be persisted globally you have to remain inside the component.
:attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.compo_state` offers you flexible storage of data on a component
level, and if that is not enough try going up through the tree via
:attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.container_compo`.

.. warning::

    Storing local data in or via the global model is the first step of a trip into confusion as long as it is nasty, since
    you have to break barriers relying heavily on understanding the EPFL Core. You will fail. Hard.
