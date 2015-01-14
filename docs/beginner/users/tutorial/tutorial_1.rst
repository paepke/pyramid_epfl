Tutorial Part 1: Basic Notes App
================================

In this tutorial, we create a simple EPFL app that provides a simple functionality to create, edit and delete notes.
For this reason, the app simply provides one view.

First, we start by creating and setting up the demo app based on an empty EPFL starter pyramid scaffold.
We create the demo app, run setup.py to set it up, and launch it using the pserve command.


.. code-block:: bash

    pcreate -s pyramid_epfl_starter demo_app
    cd demo_app/
    python setup.py develop
    pserve development.ini --reload

The app is now running on localhost:8080. If you open the URL, you will see a simple empty page displaying a "Welcome to EPFL!" message.
We will now extend this app to add the notes functionality.

You can view the final results of the complete tutorial) in a different scaffold:

.. code-block:: bash

    pcreate -s pyramid_epfl_tutorial tutorial_app
    cd tutorial_app/
    python setup.py develop
    pserve development.ini --reload
    
If you want to view both the final tutorial app and your working version (demo_app), change the port in the development.ini file 
of the tutorial app to run both server instances in parallel on your machine. 

Let's go back to our empty notes app. In demo_app/epf_pyramid_barebone/views/home.py, we will do most of the work.

In this file, we start by adding a navbar to the root component. The root component is the component that 
resides directly on the page and is basically responsible for the overall layout of the page.

In home.py, we see that the root component is instantiated as follows:

.. code-block:: python

	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(constrained=True, node_list=[epfl.components.Box(title="Welcome to EPFL!")])
	    
We change this by setting different attributes to the root_node HomeRoot object: 

.. code-block:: python

	from solute.epfl.components import NavLayout

	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(constrained=True, node_list=[NavLayout(slot='north', title='Demo Notes App')])

This replaces the box with the welcome message by a simple navbar that contains a "home" button named "Demo Notes App".
Note that by setting slot="north" in the NavLayout component, we told EPFL that this component is going to be placed in the 
top area of the parent component (this is possible since HomeRoot inherits from CardinalLayout which provides this functionality).

A lot of EPFL's components are so-called container components. They support nested components that are stored in the component's node_list attribute.

Next, we will add another component to the root component: the component that will display the form where we can create a new note or
edit an existing one.
We could do this by just extending note_list with further components when instantiating the HomeRoot class, or
by extending the HomeRoot class itself. We choose the latter way:

.. code-block:: python

	from solute.epfl.components import Box, cfForm
	
	class HomeRoot(epfl.components.CardinalLayout):
	    def init_struct(self):
	        self.node_list.extend([Box(title='My first box', node_list=[cfForm(cid='my_first_form')])])

We have now added a Box to the page that contains an empty form.

Now it's time to fill the form with live. We add form components to the form by extending its node_list:


.. code-block:: python

    from solute.epfl.components import cfText, cfTextarea, cfButton


    class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        self.node_list.extend([Box(title='My first box',
	                                   node_list=[cfForm(cid='my_first_form', node_list=[
	                                       cfText(label='Title',
	                                              name='title',
	                                              default='Insert a title here!'),
	                                       cfTextarea(label='Text',
	                                                  name='text'),
	                                       cfButton(value='Submit',
	                                                event_name='submit')])])])

If you take a look at the rendered page now, you can already see the form with its fields and the submit button. Neat!

Note that you can already experience the server-side state that EPFL provides: If you enter text in the form and click your 
browser's refresh button, the values of the form are kept.

As a next step, we want to handle the event when the user clicks on the submit button. You can add event handling methods to any component.
Ultimatively, we want to handle this event on our cfForm, since we have to react on the event and create a new note with the values of the form's fields.

Currently, the event when clicking the button is bubbled up the form. Neither the button nor the form provide an event currently, so let's add
event handling functionality to the form.
The easiest way to handle this event is by using an inherited class from cfForm: 

.. code-block:: python

    class MyFirstForm(cfForm):

        node_list = [cfText(label='Title',
                            name='title',
                            default='Insert a title here!'),
                     cfTextarea(label='Text',
                                name='text'),
                     cfButton(value='Submit',
                              event_name='submit')]
                              
	class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        self.node_list.extend([Box(title='My first box',
	                                   node_list=[MyFirstForm(cid = 'my_first_form')])])

Nothing has changed so far, we have just moved the form to our own subclass from cfForm.

We now add the event handling method to the form. Since the button is instanciated with the value "submit"
of its attribute "event_name", epfl expects a method "handle_submit" to call for event handling. We provide this
method in our FirstFormClass:

.. code-block:: python

	class MyFirstForm(cfForm):
	
		...
    
	    def handle_submit(self):
	        if not self.validate():
	            self.page.show_fading_message('An error occurred in validating the form!', 'error')
	            return
	        print self.get_values()

What happens in handle_submit()? First, the form is validated. If validation fails (both input fields are mandatory, so validation fails
if a field is empty), an error message is displayed on the page. If validation succeeds, the form values are printed on the server console.

Next, we need to do something with the actual data that comes from the form. Enter ModelBase.
All classes inheriting from ModelBase serve as a kind of interface between the data layer (e.g. database connectors etc), and the view
(i.e. the epfl components). Since we don't want to use a full-blown database in this tutorial, we will use the ModelBase to simple implement 
an in-memory storage of our notes data.

We first create our class MyModel that will serve for storing, loading and removing notes, and insert the class to our page so it is accessible later:

.. code-block:: python

	from solute.epfl.core.epflassets import ModelBase

    class MyModel(ModelBase):
        pass

    @view_config(route_name='home')
    class HomePage(epfl.Page):
        root_node = HomeRoot(
        	constrained=True, node_list=[NavLayout(slot='north', title='Demo Notes App')])
        model = MyModel


.. code-block:: python

    def handle_submit(self):
        if not self.validate():
            self.page.show_fading_message('An error occurred in validating the form!', 'error')
            return
        values = self.get_values()
        self.page.model.add_note({'title': values['title'],
                                  'text': values['text']})


.. code-block:: python

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        self.data_store['notes'].append(note)

.. code-block:: python

    def load_notes(self, calling_component, *args, **kwargs):
        print self.data_store.get('notes', [])
        return self.data_store.get('notes', [])

.. code-block:: python

    node_list = [Box(title='My first box',
                     node_list=[MyFirstForm()]),
                 LinkListLayout(get_data='notes',
                                data_interface={'id': None,
                                                'url': 'note?id={id}',
                                                'text': 'title'},
                                slot='west')]

.. code-block:: python

    Box(title='My notes',
        default_child_cls=ComponentBase(template_name='epfl_pyramid_barebone:templates/my_template.html'),
        get_data='notes')

.. code-block:: python

.. code-block:: python

.. code-block:: python

.. code-block:: python

.. code-block:: python

.. code-block:: python

.. code-block:: python

.. code-block:: python
