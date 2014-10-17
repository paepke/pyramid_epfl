=============
EPFL barebone
=============


Let's start with the smallest EPFL-application possible!

We are starting with the standard pyramid "starter" scaffold. We transform the project step by step into an EPFL application. The result is already available as pyramid_epfl_starter (as described in :ref:`barebone-scaffold`) but for didatic reasions here is how the EPFL app differs from the pure pyramid app.

A little bit of experience with `pyramid <http://www.pylonsproject.org/>`_ and `jinja2 <http://jinja.pocoo.org/docs/dev/>`_ is helpfull here!

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

        pcreate -s starter epfl_barebone
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

You can invoke now the setup.py to setup the newly created application:

    .. code:: bash

        python setup.py develop


Let's continue modifying the application:

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

    - includes and initializes EPFL (line 17) - could also be done in "development.ini pyramid.includes".
    - adds the "home"-route as part of this example (line 19)
    - initializes the beaker session-system (lines 21 and 22)
    - initializes authentication and authorization (lines 24-27)
    - sets up temp-data and nodeglobal-data providers (lines 29-33)
      
    Note: EPFL needs pyramid conform session, authentication and authorization handling, this example uses beaker and the standard pyramid authX-subsystems. EPFL also needs a machinery to store temporary-data (using local memory in this example) and some kind of shared state (also using local memory in this example).


Pages and templates
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

Create a file called home.py in the views-folder:

    .. code:: python

        #* encoding: utf-8

        from pyramid.view import view_config
        from solute import epfl


        @view_config(route_name='home')
        class HomePage(epfl.Page):

            template = "home.html"

            def setup_components(self):
                pass

You should be able to guess what is implemented here. A EPFL-application consists of "Pages" (hooked into pyramid as views). A page has a template which is used to render it self. Pages contain components which are setup by the page. Here in this example our page does not have any components (yet).
Now your application consists of one Page "HomePage" which is called as view "home" which uses a template called "home.html". Of course you have to provide this template now.

Create a file called home.html in the templates-folder:

    .. code-block:: html

        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
        <html lang="en">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <title>My first EPFL application</title>
                {{ css_imports() }}
        </head>
        <body>

            A "Hello" from the EPFL-application!

            {{ js_imports() }}

        </body>

For the sake of simplicity we did not split this template up into a "base-template" and a "page-template" - this is normally done with jinja2-blocks but not original to EPFL. 

The interesting bits here are {{ css_imports() }} and {{ js_imports() }}. Every EPFL-page needs those. Since an EPFL-Page normally contains components - which themselves consist of HTML, JS and CSS, the system collects and puts the CSS and JS into these places. Just make sure, that the {{ css_imports() }} is in the head of the template and the {{ js_imports() }} is at the bottom of the body.

Let's invoke this little application!
    
    .. code-block:: bash

        cd WHERE_THE_PROJECT_IS
        pserve development.ini --reload


.. figure:: /_static/empty_app.png
    :width: 50%
    :align: center

    This is what you should get at http://localhost:6543/

Not so much, really!

Let's spice this up a little bit...

Components
----------

Adapt the views/home.py as follows:

    .. code:: python

        ...

        class MyForm(epfl.components.Form):

            name = epfl.fields.Entry("Name", type = "char(128)", mandatory = True)
            ok = epfl.fields.Button("OK")

        ...


    .. code:: python

        ...

        @view_config(route_name='home')
        class HomePage(epfl.Page):

            ...

            def setup_components(self):
                
                self.my_form = MyForm()

Components in EPFL are subclasses of so called "base-components" which themselves are subclasses of :class:`~solute.epfl.core.epflcomponentbase.ComponentBase`. In this example, we created a component called "MyForm" derived from a "Form"-base-component. The form is configured by overwriting and adding component-specific class-attributes. In the case of a form, we add fields.

The components then are assinged to the page by creating them in the "setup_components"-method of the page. This method is called by EPFL, everytime it needs to know the components of this page.

Now the page knows about the form-component "MyForm". We must now tell the system where to render it. This is done in the template:

    .. code-block:: html

        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
        <html lang="en">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <title>My first EPFL application</title>
                {{ css_imports() }}
        </head>
        <body>

            A "Hello" from the EPFL-application!

            <div style="width:50%;margin:auto;background:#ddd">
                {{ my_form.render() }}
            </div>


            {{ js_imports() }}

        </body>

Go to your browser and hit F5!

.. figure:: /_static/first_app_1.png
    :width: 50%
    :align: center

    This is what you should get at http://localhost:6543/

Not very pretty, but you should get the point. 

For now we do not go into details how to modify the layout of the form. Let's add some action instead...


Events and server-side-state
----------------------------

Adapt the views/home.py as follows:

    .. code:: python

        ...

        class MyForm(epfl.components.Form):

            ...

            ok = epfl.fields.Button("OK", on_click = "ok")

            def handle_ok(self):
                if self.validate():
                    self.show_fading_message("Hello {name}".format(name = self.name.data))

                self.redraw()

        ...

    The changes are: add an "on_click" to the Button-definition, add the event-handler "def handle_ok"


.. figure:: /_static/first_app_2.png
    :width: 50%
    :align: center

    Clicking "OK"-Button with empty "Name" field.

.. figure:: /_static/first_app_3.png
    :width: 50%
    :align: center

    Clicking "OK"-Button with correctly filled "Name" field.

EPFL supports an event-driven programming style. Components and fields (e.g. a button of a form) provide predefined events (e.g. "on_click") on which you can bind commands (in this example "ok"). When the event is fired (the user clicks the button) the event-handler of the component is invoked. An event-handler is a method of the component-class and always named "handle_XXX", where XXX is the name of the command. Since we have server-side-state (explained later) the value of the form-field "name" is always available on server-side as "self.name.data".

Form validation - as feature of the form-base-component - is also done. The call to "self.validate()" does two things. As a side-effect it updates the error-state of each visible form-field according to the current field-value. If all validators - explicit ones given by the programmer and implicit ones entailed by the field-type - succeed the validator returns "True", if only one validator fails it returns "False".

The "self.redraw()" call marks the component as "queued for redraw". When EPFL sends back the response to the browser it collects all components in is queue, renders them and sends back the new HTML and JS. At client side the HTML of the component is replaced with the new one and the JS is executed. Since the EPFL-core by design does not use a listener/observer technique you have to redraw your components manually. In this case because you want to see the error-messages of the mandatory field "name" appear and disappear.

Finally, what does "server-side-state" mean? Every change made at client side (normally by a user typing in data or clicking somewhere) is replicated automatically to the server side. Also changes made at server side (normally by event handlers source code) is replicated back to the client - by redrawing components. So as a programmer you always can be sure to have all the state of the application at your fingertips at server side. Even across pages when the page is no longer available at client side. No need to submit forms, handle cookies, persist/update data in the session. Superb!

.. _barebone-scaffold:

Barebone scaffold
-----------------

Congratulations! You just wrote and understood your first EPFL-application. You did this the hard way starting with an original pyramid-scaffold. 

For convenience we provide a EPFL barebone scaffold: This scaffold is intended as starting point for your project. It is as empty as possible!
You are highly encouraged to use the pre-build EPFL barebone scaffold instead of manually doing all steps as described above:

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

If you want to see a more demonstrating application you can use the "memo-application"-scaffold as described in :doc:`../installation`.


What next?
----------

- :doc:`Understand other concepts of the framework. <concepts>`
- :doc:`Take a tour throu the existing base-components! </components/index>`
- :doc:`How to design your own application? <app_design>`
- :doc:`Check the limitations of an EPFL-application. <limitations>`
  
