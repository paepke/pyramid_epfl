.. _quickstart:

Quickstart for EPFL ...
=======================


.. _quickstart_users:

... users
---------

You need

- "python" (should be already on your box)
- "virtualenv" (sudo apt-get install python-virtualenv)
- "pip" (sudo apt-get install python-pip)
- "curl" (sudo apt-get install libcurl4-gnutls-dev)

installed. EPFL itself can easily be installed with pip, and you can safely disregard, everything before pip install if
you are not using virtualenv (which is however strongly suggested).

    .. code-block:: bash

        mkdir epfl; cd epfl
        virtualenv env
        source env/bin/activate
        pip install pyramid-epfl

If you want to you can also checkout EPFL from `the github repository`_ and install it with

    .. code-block:: bash

        git clone https://github.com/solute/pyramid_epfl.git
        cd pyramid_epfl
        python setup.py install


To help with getting started EPFL provides a special pyramid scaffold which can be installed with

    .. code-block:: bash

        pcreate -s pyramid_epfl_starter MyFirstEPFLProject
        cd MyFirstEPFLProject
        python setup.py develop
        pserve development.ini

The freshly created MyFirstEPFLProject contains a basic example for using EPFL productively.

Have fun at http://localhost:6543/


.. _quickstart_component_developers:

... component developers
------------------------

Developing components for EPFL is easy, just checkout EPFL from `the github repository`_ and install it, then create an
example Project using the pyramid_epfl_starter scaffold:

    .. code-block:: bash

        git clone https://github.com/solute/pyramid_epfl.git
        cd pyramid_epfl
        python setup.py develop
        cd ..
        pcreate -s pyramid_epfl_starter MyFirstEPFLProject
        cd MyFirstEPFLProject
        python setup.py develop
        pserve development.ini

In order to get a feel for the behaviour of components try experimenting a bit with the example, switching out templates
and manipulating the default behaviour of existing components.


.. _quickstart_core_developers:

... core developers
-------------------

Well, there's good news and there's bad news for you. The good news is: All you need to do is basically the same as any
component developer.

The bad news is: While a component developer generally has a clear cut section of work to do, the core is everywhere.
The core has many an appendix, but the most important parts are:
 - :class:`solute.epfl.core.epflcomponentbase.UnboundComponent`
 - :class:`solute.epfl.core.epflcomponentbase.ComponentBase`
 - :class:`solute.epfl.core.epflcomponentbase.ComponentContainerBase`
 - :class:`solute.epfl.core.epflpage.Page`
 - :class:`solute.epfl.core.epfltransaction.Transaction`

Understanding these and their sometimes complex interweaving is paramount to safely fix bugs, improve existing core
features or implement new ones. If you are new here, you best start with writing a couple of Components. If you feel
confident in your grasp of those you can proceed here: :ref:`into_the_core`


.. _the github repository: http://github.com/solute/pyramid_epfl