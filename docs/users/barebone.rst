=============
EPFL barebone
=============


Let's start with the smallest EPFL-application possible!

First off, install EPFL and it's dependencies like that (including pyramid):

    .. code:: bash

        cd WHEREEVER_YOU_WANT
        virtualenv env
        source env/bin/activate    
        pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl

Now you got EPFL besides a working Pyramid installation. That was easy!

Next we use the standard pyramid scaffold mechanism to create a pyramid-app:

    .. code:: bash

        pcreate -s pcreate -s starter epfl_barebone
        cd epfl_barebone

Nothing new to a pyramid user up to this point.

Now let's adapt some configs and dependencies:

    *test.py:*

    .. code:: python

        print "LALA!!"


Then we add the EPFL-specific parts:

