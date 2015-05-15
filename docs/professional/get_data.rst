.. _get_data:

How do I get data?
==================
The get_data convenience methods are the way of choice to provide data from any API, Database or other Datasource to
EPFL and its components.


The basics
----------
You probably have followed these instructions more than once:

.. automethod:: solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data
    :noindex:

The actual mechanism enabling this method is in
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase._get_data`:

.. code-block:: python

    def _get_data(self, *args, **kwargs):
        """
        Internal wrapper for :meth:`get_data` to decide wether it is to be called as a function or only contains a
        reference to a model on :attr:`.epflpage.Page.model`.
        """
        # get_data is a string pointing to a model load function.
        if type(self.get_data) is str and self.page.model is not None:
            return self.page.model.get(self, self.get_data, (args, kwargs), self.data_interface)
        # get_data is a tuple with a string or integer pointing to a model and a string pointing to a model load
        # function.
        elif type(self.get_data) is tuple and self.page.model is not None:
            return self.page.model[self.get_data[0]].get(self, self.get_data[1], (args, kwargs), self.data_interface)
        # default: get_data is a callable.
        return self.get_data(*args, **kwargs)

The three cases are separated here and put into the correct pipelines.

Default handling
................
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data` is called and its return value is used as
data inside :meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.update_children`:

.. code-block:: python

    data = self._get_data(self.row_offset, self.row_limit, self.row_data)

The data is then used to either update existing components:

.. code-block:: python

    # IDs of data represented by a component. Matching components are updated.
    for data_id in set(new_order).intersection(current_order):
        compo = getattr(self.page, data_cid_dict[data_id])
        for k, v in data_dict[data_id].items():
            if getattr(compo, k) != v:
                setattr(compo, k, v)
                self.redraw()

or used as attributes to create completely new components:

.. code-block:: python

    # IDs of data not yet represented by a component. Matching components are created.
    for data_id in set(new_order).difference(current_order):
        ubc = self.default_child_cls(**data_dict[data_id])
        bc = self.add_component(ubc, init_transaction=init_transaction)
        data_cid_dict[data_id] = bc.cid

        self.redraw()

In every case data needs to be a Sequence of Mappings.

Loading from a model
....................
This method is straight forward and implemented in :meth:`~solute.epfl.core.epflassets.ModelBase.get` in
:class:`~solute.epfl.core.epflassets.ModelBase`. This method is one you have very probably never seen before, since it
is most definitely a part of the core. While overwriting :class:`~solute.epfl.core.epflassets.ModelBase` is required to
provide data, the :meth:`~solute.epfl.core.epflassets.ModelBase.get` is accessed only by
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase._get_data`.


Update children
---------------
