.. cycling_epfl:

Cycling EPFL: Life of a request
===============================
Previously this topic was kind of a hassle. There were actually a hand full of ways any request might walk through a
given :class:`~solute.epfl.core.epflpage.Page` call. Thankfully we've had time to rearrange this a bit so take a look:

.. code-block:: python

    def __call__(self):
        """
        The page is called by pyramid as view, it returns a rendered page for every request. Uses :meth:`call_ajax`,
        :meth:`call_default`, :meth:`call_cleanup`.
        [request-processing-flow]
        """

        self.setup_model()

A model for everyone
--------------------
Previously EPFL was utilizing the reflection mechanisms of pyramid (and thus zope) to allow a user the creation of
custom data sources. But since actually meddling with the config is frowned upon nowadays (there's really only a blessed
few processes that absolutely require this still) a new solution had to be found. The new
:class:`~solute.epfl.core.epflassets.ModelBase` is a simple base class for all the needs anyone might ever have. It's
tightly tied into the get_data pattern you should know well from working with
:class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase` and its offspring before. You can find more
information on this mechanism in its own topic: :ref:`get_data`

.. code-block:: python

        # Check if we lost our transaction to a timeout.
        transaction_loss = self.prevent_transaction_loss()
        if transaction_loss:
            return transaction_loss


Only you can prevent transaction loss!
--------------------------------------
Since EPFL does no longer carry its own specific session handler some instances have arisen where transactions were
partially or completely lost. This little helper function checks if the transaction is still well formed and if not
creates a page reload in order to avoid exceptions and crashes from a malformed
:class:`~solute.epfl.core.epfltransaction.Transaction`.


.. code-block:: python

        self.handle_transaction()

Recursive statements are recursive because they are Recursions
--------------------------------------------------------------
This call is the first actual stepping stone in the official lifecycle. It invokes the following methods:
 1. :meth:`solute.epfl.core.epflpage.Page.setup_components` is called to assign the root_node.
 2. If the root_node has not already been initialized in this :class:`~solute.epfl.core.epfltransaction.Transaction`
    its :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction` method is called.
 3. Any currently active component, that is components that have been instantiated during this phase, are then also
    initialized as necessary by calling their respective
    :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction` methods as well.

These three steps build the lifecycle stage usually referred to as "init transaction" or similar names.

.. code-block:: python

        content_type = "text/html"

        if self.request.is_xhr:
            self.handle_ajax_events()
            content_type = "text/javascript"
        else:
            # Reset the rendered_extra_content list since none actually has been rendered yet!
            self.transaction['rendered_extra_content'] = set()
            self.handle_default_events()

        for compo in self.get_active_components():
            compo.after_event_handling()

        out = self.render()

        out += self.call_cleanup(self.request.is_xhr)

        response = Response(body=out.encode("utf-8"),
                            status=200,
                            content_type=content_type)
        response.headerlist.extend(self.remember_cookies)
        return response