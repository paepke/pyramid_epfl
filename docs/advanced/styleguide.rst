===========
Style Guide
===========

In order to usefully contribute to EPFL please adhere to the following style guide for components! For your convenience:
 * **must** is used to describe absolute requirements from which deviations will not be accepted.
 * **should** is used to describe requirements from which deviations will be accepted if a reason is given.
 * **may** is used to describe optional parts that can be left out or ignored.

Folder structure
----------------

 1. The component **must** be inside a folder with its name in lowercase with _ for word separation in the
    solute/epfl/components directory. This is referred to as the lowercase component name. Example: cardinal_layout,
    context_list_layout, button
 2. The primary content of the component **must** be in a file named <lowercase component name>.py
 3. If the component has set its :attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.asset_spec` to its own
    location the directory **must** contain a sub folder named static.


Dynamic Javascript
------------------
If a file named <lowercase component name>.js exists in the components directory it **must** begin like this:

.. code-block:: javascript

    epfl.init_component("{{ compo.cid }}", "<camelcase component name>"


Static Javascript
-----------------
If a file named <lowercase component name>.js exists in the components static directory it:

 1. **Must** begin with:

     .. code-block:: javascript

         epfl.<camelcase component name> = function(cid, params)

 2. **Must** contain a call to its base component from which it inherited (normally ComponentBase):

     .. code-block:: javascript

         epfl.<camelcase base component name>.call(this, cid, params);

 3. **Must** contain an inheritance denominator:

     .. code-block:: javascript

         epfl.<camelcase component name>.inherits_from(epfl.<camelcase base component name>);

 4. **May** contain functions overwriting lifecycle methods set via the prototype mechanism which **should** call the base
    components super method:

     .. code-block:: javascript

         epfl.<camelcase component name>.prototype.before_request = function() {
            epfl.<camelcase base component name>.prototype.before_request.call(this);
         };

         epfl.<camelcase component name>.prototype.before_response = function(data) {
            epfl.<camelcase base component name>.prototype.before_response.call(this, data);
         };

         epfl.<camelcase component name>.prototype.after_response = function() {
            epfl.<camelcase base component name>.prototype.after_response.call(this);
         };

 5. **May** contain additional functions set via the prototype mechanism:

     .. code-block:: javascript

         epfl.<camelcase component name>.prototype.<fn name> = function() {};


Python Code
-----------
Inheritance
^^^^^^^^^^^
The main python file **should** contain a single class of the camelcase component name. It **must** be inheriting from
:class:`solute.epfl.core.epflcomponentbase.ComponentBase`,
:class:`solute.epfl.core.epflcomponentbase.ComponentContainerBase` or another component inheriting from either of them.

The __init__ method
^^^^^^^^^^^^^^^^^^^
The component class **must** contain an __init__ method which **must** use these minimum 3 parameters in the given
order:

 1. self
 2. page
 3. cid

The method also **must** use at least one the following parameters:

 1. \*\*kwargs
 2. \*\*extra_args

The method **may** contain the additional parameter \*args.

The __init__ method **must** contain a docstring with a short description of the component. The docstring **should**
contain a usage example. The docstring **must** contain a parameter description for any parameter other than the
aforementioned.

Example:

.. code-block:: python

    class ExampleComponent(solute.epfl.epflcomponentbase.ComponentBase):
        def __init__(self, page, cid, some_param=None, **extra_args):
            """This is an example component that really does nothing. Use it like this:

            ExampleComponent(
                cid='example_component',
                some_param=False,
            )

            :param some_param: This param does something, it can be set to None, True or False.
            """

The __init__ method **should** be the first method in any component.

Custom Attributes
^^^^^^^^^^^^^^^^^
All custom attributes declared within that class **must** be decorated with a docstring in one of these styles:

.. code-block:: python

    class ExampleComponent(solute.epfl.epflcomponentbase.ComponentBase):
        example_attribute = None  #: This is an example attribute, which does nothing.

        #: This is another example attribute, which still does nothing.
        second_example_attribute = None

        #: This is yet another example attribute, which still does nothing.
        #: But since the text is long it is split into multiple lines.
        third_example_attribute = None

Custom attributes that are intended to be parametrized by the user on component instantiation **must** be named
arguments in the components __init__ method.

Special Attributes or Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All components **must not** set specific values to the following attributes:

 1. cid
 2. slot

These values are reserved for the EPFL core.

All components **should not** set specific values to the following attributes or methods:

 1. :attr:`solute.epfl.core.epflcomponentbase.ComponentBase.post_event_handlers`
 2. :meth:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data`

These values are usually reserved for the application developer.

All components derived from :class:`solute.epfl.core.epflcomponentbase.ComponentContainerBase` **should** provide the
following attributes as appropriate:

 1. :attr:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.default_child_cls`
 2. :attr:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.data_interface`


Lifecycle methods
^^^^^^^^^^^^^^^^^
Basic Lifecycle Methods
"""""""""""""""""""""""
All components **may** provide their own implementation of any of the following methods from
:class:`solute.epfl.core.epflcomponentbase.ComponentBase`:

  1. :meth:`solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction`
  2. :meth:`solute.epfl.core.epflcomponentbase.ComponentBase.setup_component`
  3. :meth:`solute.epfl.core.epflcomponentbase.ComponentBase.after_event_handling`

If provided any such implementation **should** call its respective super method at the appropriate time.

All components **may** provide their own implementation of any of the following methods from
:class:`solute.epfl.core.epflcomponentbase.ComponentContainerBase`:

 1. :meth:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_struct`
 2. :meth:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_transaction`

If provided any such implementation **should** call its respective super method at the appropriate time.

If provided these methods **should** be in the given order directly after the __init__ method.

Any of the aforementioned implementations **may** contain a doc string to briefly summarize the actions taken at this
time by this component.

Event Handling
""""""""""""""
All components **may** provide event handling methods. Any event handling method **must** be prefixed with
"handle\_". Any such method **should** contain a doc string in the style of the __init__ method. If provided by a
component in the inheritance chain any such implementation **should** call its respective super method at the
appropriate time.

All components **should not** provide post event handling methods. These methods **must** be prefixed with "on\_". Any
such method **should** contain a doc string in the style of the __init__ method. If provided by a component in the
inheritance chain any such implementation **should** call its respective super method at the appropriate time. Post
event handling **should** be left to the application developer.
