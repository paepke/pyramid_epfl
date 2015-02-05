.. components:

EPFL components
===============

At its core EPFL components are a simple thing: They have visual code, are filled with data and then interact with that
data and its sources based on user interaction. While simple on the outside the number of convenience layers complicates
handling components in the core to a somewhat large degree.

Binding components
------------------

.. code-block:: python

    class MyRootNode(ComponentContainerBase):
        node_list = [Box(cid='my_box',
                         title='My Box!')]

        def setup_component(self):
            print self.page.my_box

    @view_config(route_name='data')
    class MyPage(Page):
         root_node = MyRootNode()

You have seen this time and again, as a developer using EPFL or even as a component developer what is going on here is
not of great importance to you. Inside the core however there's a lot going on. Depending on where you got Box from this
could take three separate ways until it actually ends up as a bound and initialized component available via
self.page.my_box. Let's take a look where this all starts: In the :class:`solute.epfl.core.epflpage.Page`.

.. code-block:: python

    def setup_components(self):
        """
        Overwrite this function!
        In this method all components needed by this page must be initialized and assigned to the page (self). It is
        called only once per transaction to register the "static" components of this page. No need to call this (super)
        method in derived classes.

        [request-processing-flow]
        """
        self.root_node = self.root_node(self, 'root_node', __instantiate__=True)

The oddity is easily visible: __instantiate__. Unless you deviated quite far from best practices you probably have never
seen this flag used when calling a component before. It is used only if you are assigning a component to a
:class:`~solute.epfl.core.epflpage.Page` statically.

Looking under the hood of this call you'll first have to figure out what you are actually dealing with in
self.root_node. It might be any of two things, an |unbound_compo| instance or a |compo_base| class object.

Usually you'd find an |unbound_compo| instance and not a sub-class of |compo_base|. This is due to a simple trick:

.. code-block:: python

    def __new__(cls, *args, **config):
        """
        Calling a class derived from ComponentBase will normally return an UnboundComponent via this method unless
        __instantiate__=True has been passed as a keyword argument.

        Any component developer may thus overwrite the :func:`__init__` method without causing any problems in order to
        expose runtime settable attributes for code completion and documentation purposes.
        """
        if config.pop('__instantiate__', None) is None:
            return UnboundComponent(cls, config)
        [...]

Any sub-class of |compo_base| will yield an
|unbound_compo| instance if called without that parameter.

+-----------------------------------------------------------+
| So there's a huge difference between those two            |
+-----------------------------+-----------------------------+
|.. code-block:: python       |.. code-block:: python       |
|                             |                             |
|    root_node = MyRootNode() |    root_node = MyRootNode   |
+-----------------------------+-----------------------------+
| an |unbound_compo| instance | and a |compo_base| sub-class|
+-----------------------------+-----------------------------+

Thus when defining components you are usually working with |unbound_compo| instances. Those will be converted to
|compo_base| instances during the :meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_transaction`
call of any :class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase` sub-class. So there's two ways to follow
for the call of :meth:`solute.epfl.core.epflpage.Page.setup_components`.

Any |unbound_compo| instance is a callable, thus the instantiation will be handled by
:meth:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__call__`.

.. code-block:: python

    # solute/epfl/core/epflcomponentbase.py
    def __call__(self, *args, **kwargs):
        """
        Pseudo instantiation helper that returns a new UnboundComponent by updating the config. This can also be used to
        generate an instantiated Component if one is needed with the __instantiate__ keyword set to True.
        """
        if kwargs.pop('__instantiate__', None) is None:
            config = self.__unbound_config__.copy()
            config.update(kwargs)
            return UnboundComponent(self.__unbound_cls__, config)
        else:
            self.__unbound_config__.update(kwargs)
            self.__dynamic_class_store__ = None
            kwargs['__instantiate__'] = True

        cls = self.__dynamic_class__
        return cls(*args, **kwargs)

If no instantiation is in process calling any |unbound_compo| will simply return a new instance with its config updated.
Otherwise this updates the configuration, empties the
:attr:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__dynamic_class_store__` then uses the property
:attr:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__dynamic_class__` to dynamically generate a python
type-class that is then used to create an instance of this |compo_base| sub-class.


.. |unbound_compo| replace:: :class:`~solute.epfl.core.epflcomponentbase.UnboundComponent`
.. |compo_base| replace:: :class:`~solute.epfl.core.epflcomponentbase.ComponentBase`

.. _Traversal: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html
.. _`URL Dispatch`: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/urldispatch.html
.. _odict: https://github.com/therealfakemoot/collections2
.. _collections2: https://github.com/therealfakemoot/collections2
