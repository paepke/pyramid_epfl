
==========
Quickstart
==========

You need 

- "python" (should be already on your box)
- "virtualenv" (sudo apt-get install python-virtualenv)
- "pip" (sudo apt-get install python-pip)
- "curl" (sudo apt-get install libcurl4-gnutls-dev)

installed.

Open a shell in your Linux box and...

    .. code:: bash

        mkdir epfl; cd epfl
        virtualenv env
        source env/bin/activate
        pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl
        pcreate -s pyramid_epfl_notes notes_app
        cd notes_app
        python setup.py develop
        pserve development.ini


Have fun at http://localhost:6543/


