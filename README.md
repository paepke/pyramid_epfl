==========================
EPFL Python Frontend Logic
==========================

To install:
-----------

	mkdir epfl; cd epfl
	virtualenv env
	source env/bin/activate
	pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl
	pcreate -s pyramid_epfl_starter barebone
	cd barebone
	python setup.py develop
	pserver development.ini




