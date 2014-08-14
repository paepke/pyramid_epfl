=============
EPFL barebone
=============


Let's start with the smallest EPFL-application possible!

We are starting with the standard pyramid "starter" scaffold. We transform the project step by step into an EPFL application. The result is already available as pyramid_epfl_starter (as described in :ref:`barebone-scaffold`) for convenience but here is how the pure pyramid app differs from an EPFL app.

Pyramid scaffold
----------------

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

Configs
-------

Now let's adapt some configs and dependencies in the project directory:

    *setup.py:*

    .. code-block:: python
        :emphasize-lines: 3, 4, 8, 9

        requires = [
            'pyramid',
            'pyramid_beaker',
            'pyramid_jinja2',
            'pyramid_chameleon',
            'pyramid_debugtoolbar',
            'waitress',
            'wtforms',
            'ujson',
            ]

    Just add the highlighted lines to your setup.py. This tells pyramid to setup beaker (for sessions and cache) and jinja2 (for templating), wtforms (base for the epfl-forms) and ujson (needed everywhere).

    *development.ini:*

    .. code-block:: bash

        [app:main]
        ...
        pyramid.includes =
            pyramid_debugtoolbar
            pyramid_jinja2
            pyramid_beaker
        ...

        ...
        jinja2.directories = templates
        jinja2.extensions = solute.epfl.jinja.jinja_extensions.EpflComponentExtension

        # Beaker cache
        cache.regions = default_term, second, short_term, long_term
        cache.type = memory
        cache.second.expire = 1
        cache.short_term.expire = 60
        cache.default_term.expire = 300
        cache.long_term.expire = 3600

        # Beaker sessions
        session.type = memory
        session.key = epfl_barebone
        session.secret = 0cb243e53ad865a0f70099c0414ffe9cfcfe03ac

        epfl.debug = true

    Modify your development.ini accordingly. Change the pyramid.includes-list and add the missing parts to the [app:main] section. Changes are: including jinja2 and beaker, telling jinja2 where to get the templates and it's extensions, setup beaker both cache and sessions and telling
    epfl to use debug-mode.

    *epfl_barebone/__init__.py:*

    .. code-block:: python
        :linenos:        

        #* coding: utf-8

        from pyramid.config import Configurator

        from pyramid_beaker import session_factory_from_settings


        from pyramid.authentication import AuthTktAuthenticationPolicy
        from pyramid.authorization import ACLAuthorizationPolicy

        from solute.epfl import epfltempdata

        def main(global_config, **settings):
            """ This function returns a Pyramid WSGI application.
            """
            config = Configurator(settings=settings)
            config.include("solute.epfl")

            config.add_route('home', '/')    
            
            session_factory = session_factory_from_settings(settings)    
            config.set_session_factory(session_factory)

            authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
            authz_policy = ACLAuthorizationPolicy()
            config.set_authentication_policy(authn_policy)
            config.set_authorization_policy(authz_policy)

            temp_data_provider = epfltempdata.LocalMemoryProvider(config)
            config.set_tempdata_provider(temp_data_provider)

            nodeglobal_data_provider = epfltempdata.LocalMemoryProvider(config)
            config.set_nodeglobaldata_provider(nodeglobal_data_provider)
            
            config.scan()
            return config.make_wsgi_app()

    Replace the complete file with this content. It does the following:

    - includes and initializes EPFL (line 17)
    - adds the "home"-route as part of this example (line 19)
    - initializes the beaker session-system (lines 21 and 22)
    - initializes authentication and authorization (lines 24-27)
    - sets up temp-data and nodeglobal-data providers (lines 29-33)
      
    Note: EPFL needs pyramid conform session, authentication and authorization handling, this example uses beaker and the standard pyramid authX-subsystems. EPFL also needs a machinery to store temporary-data (using local memory in this example) and some kind of shared state (also using local memory in this example).


Views and templates
-------------------

Now it's time to add some pages, templates and components to our application. Again we start from the pyramid-starter scaffold and modify it accordingly.

Delete the following files from your project, they are not needed by our applcation:

    - <project-folder>/epfl_barebone/static/*
    - <project-folder>/epfl_barebone/templates/mytemplate.pt
    - <project-folder>/views.py

Create a folder:

    - <project-folder>/views

and put an empty __init__.py file in it.

Then we add the EPFL-specific parts:


.. _barebone-scaffold:

Barebone scaffold
-----------------


To use the pre-build EPFL barebone scaffold:

    .. code:: bash

        mkdir epfl; cd epfl
        virtualenv env
        source env/bin/activate
        pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl
        pcreate -s pyramid_epfl_starter barebone
        cd barebone
        python setup.py develop

    You may start up the barebone at http://localhost:8080/ with (but there is really not much to see!):

    .. code:: bash

        pserve development.ini



