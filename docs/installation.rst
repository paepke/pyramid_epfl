============
Installation
============

You need "python", "virtualenv" and "pip" installed.

Open a shell in your Linux box and...

    .. code:: bash

        mkdir epfl; cd epfl
        virtualenv env
        source env/bin/activate
        pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl
        pcreate -s pyramid_epfl_notes notes
        cd notes
        python setup.py develop
        pserve development.ini


Have fun!

