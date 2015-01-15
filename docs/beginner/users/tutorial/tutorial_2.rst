.. _tutorial_2:

Tutorial Part 2: Notes App with nested notes
============================================

In part 2 of the tutorial, we continue with the notes app we have created in part 1.
You can directly extend the code you ended up with after completing part 1.

In this part, we will extend our notes app with nested notes, that means a note can have multiple child notes which can itself have child notes, and so on.
For this, we can specify the parent id of a note when creating or editing it, and the notes list displays nested notes in a tree-like view.

Let's start by adapting our NoteModel to reflect child notes: 

.. code-block:: python

	class NoteModel(ModelBase):
	    data_store = {'_id_counter': 1,
	                  '_id_lookup': {}}
	
	    def add_note(self, note):
	        note['id'] = self.data_store['_id_counter']
	        self.data_store['_id_counter'] += 1
	        note.setdefault('children', [])
	
	        self.data_store['_id_lookup'][note['id']] = note
	
	        if 'parent' in note and note['parent'] != 0:
	            self.get_note(note['parent']).setdefault('children', []).append(note['id'])
	        else:
	            self.data_store.setdefault('notes', []).append(note)
	
	    def remove_note(self, note_id):
	        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]
	        parent_id = self.data_store['_id_lookup'].pop(note_id)['parent']
	        if parent_id != 0:
	            self.get_note(parent_id)['children'].remove(note_id)
	
	    def get_note(self, note_id):
	        return self.data_store['_id_lookup'][note_id]
	
	    def set_note(self, note_id, value):
	        self.get_note(note_id).update(value)
	
	    def load_notes(self, calling_component, *args, **kwargs):
	        notes = self.data_store.get('notes', [])
	        return notes
	
	    def load_note_children(self, calling_component, *args, **kwargs):
	        return [self.get_note(child_id) for child_id in self.get_note(calling_component.id)['children']]

Note that we've added the parameter calling_component to the load_note_children() method.
We need this later because this method, being prefixed with "load_", will serve later for a component to obtain note children via
the get_data attribute. When this method is called then, the calling_component parameter can be used to obtain the component that has 
called, and obtain the note children for the calling components note. We well dig into that a little later.
	        
Up to now, nothing has changed in our page. Notes are still created and displayed as before.
Let's add functionality to set the parent id of a note.
This is a straightforward extension of our NoteForm class:

.. code-block:: python

	from solute.epfl.components import cfNumber

	class NoteForm(cfForm):
	
	    node_list = [cfNumber(label='Parent note id',
	                          name='parent'),
	                 cfText(label='Title',
	                        name='title',
	                        default='Insert a title here!'),
	                 cfTextarea(label='Text',
	                            name='text'),
	                 cfButton(value='Submit',
	                          event_name='submit')]
	    ...
		
	    def handle_submit(self):
	        if not self.validate():
	            self.page.show_fading_message('An error occurred in validating the form!', 'error')
	            return
	        values = self.get_values()
	        note_value = {'parent': values['parent'],
	                      'title': values['title'],
	                      'text': values['text']}
	        if self.id is None:
	            self.page.model.add_note(note_value)
	        else:
	            self.page.model.set_note(self.id, note_value)
	        self.clean_form()
	
	    def handle_cancel(self):
	        self.clean_form()
	
	    def clean_form(self):
	        self.id = None
	        self.set_value('title', '')
	        self.set_value('text', '')
	        self.set_value('parent', 0)
	        self.redraw()
	
	    def load_note(self, note_id):
	        note = self.page.model.get_note(note_id)
	        self.id = note['id']
	        self.set_value('parent', note['parent'])
	        self.set_value('title', note['title'])
	        self.set_value('text', note['text'])
	        self.redraw()
	        
Now for the fun part.
We now extend our NoteBox to display nested notes.
Up to now, NoteBox was nested in a Box using default_child_cls, and it directly renders the contents of a single note.
Now, we make NoteBox nestable by setting its own default_child_cls to the very same class (we have to do this in the __init__ method to use 
this self-reference):

.. code-block:: python

	class NoteBox(Box):
	
	    def __init__(self, *args, **kwargs):
	        super(NoteBox, self).__init__(*args, **kwargs)
	        self.default_child_cls = NoteBox

And how do we set note data to the nested NoteBox elements? Using get_data, of course. Since we have defined load_note_children() in our NoteModel above,
we can refer to that now as follows: 

.. code-block:: python

	class NoteBox(Box):
	
	    def __init__(self, *args, **kwargs):
	        super(NoteBox, self).__init__(*args, **kwargs)
	        self.get_data = 'note_children'
	        self.default_child_cls = NoteBox

To make that work, we have to change the approach how a NoteBox renders the actual note contents.
Instead of using nested components that are specified in init_struct(), we enhance the template of the note.
Hence, we first remove the init_struct() method of NoteBox.

If you create components now and set the parent id of a new component to an already existing id (e.g. 1), you will see
that the notes list already renders as a nested list.
We will now improve the display by extending the NoteBox templates. We do this by extending the templates of the NoteBox parent class:

.. code-block:: python

	class NoteBox(Box):
	
		theme_path = Box.theme_path[:]
		theme_path.append('<epfl_pyramid_barebone:templates/theme/note')
		
		...
		
We can now place template files in the templates/theme/note folder that extend the templates of the parent class.
Container components such as Box come with 4 templates: container.html, after.html, before.html and row.html:

* container.html renders the outermost component
* before.html is called to render the part before the nested components are rendered
* row.html is called for each nested component 
* after.html is called to render the part after all nested components have been rendered

You don't need to override all of them, just adapt the templates you need.  
Note that the added theme path is preceded by a "<". This tells epfl that the specific note theme templates are 
rendered first and then call the corresponding parent templates for rendering afterwards.
If "<" is missing, the behaviour is the other way round.

To improve the display of our nested notes list, we just have to provide an additional before.html template in the 
templates/theme/note folder:

.. code-block:: jinja

	{% macro render() %}
	    {% set compo = kwargs.compo %}
	    {{ caller() }}
	    <p>
	        {{ compo.title }} - (ID: {{ compo.id }})
	    </p>
	    <pre>
	        {{ compo.text }}
	    </pre>
	{% endmacro %}

Note that the invocation of caller() calls the before.html template of the parent class. 

Now, our notes list display the note id, title, and text again.
And since the NoteBox has the is_removable attribute set to True, boxes and the corresponding notes can be removed again without any additional code.

The only thing that is currently still missing is the option to load notes from the notes list view in the notes form.
Our NoteBox still provides the handle_edit_note method, but it is not called since no nested button component binds to this event.
We adjust our template before.html to add a little Font-Awesome icon for this:

.. code-block:: jinja

	{% macro render() %}
	    {% set compo = kwargs.compo %}
	    {{ caller() }}
	    <i class="fa fa-lg fa-edit"></i>
	    <p>
	        {{ compo.title }} - (ID: {{ compo.id }})
	    </p>
	    <pre>
	        {{ compo.text }}
	    </pre>
	{% endmacro %}
	
Finally, we have to detect a mouse click on the edit button and invoke a EPFL event that leads to the execution of handle_edit_note.

This is done in a Javascript file that is executed for our NoteBox component in the browser.
We first specify the location and usage of the Javascript file in our NoteBox class:


.. code-block:: python

	class NoteBox(Box):
	
	    js_parts = Box.js_parts[:]
	    js_parts.append('epfl_pyramid_barebone:templates/theme/note/note.js')
	    
	    ...
	
We can now add the following note.js java script file in the templates/theme/note folder:

.. code-block:: javascript

	$('[epflid=' + '{{ compo.cid }}' + '] > div.panel-body > .fa.fa-lg.fa-edit').click(function () {
	    epfl.send(epfl.make_component_event('{{ compo.cid }}', 'edit_note'));
	});
	
This Javascript code does the following: It binds a JQuery event to the <i class="fa fa-lg fa-edit"></i> element of a NoteBox.
In order to avoid bindings to other elements, such bindings should be as explicit as possible.
Hence, only elements with those font-awesome classes that are nested in a div with "panel-body" class inside our component (which we adress by the epflid attribute)
are found.
Since we know the HTML structure of our box, we make sure that only the edit button of the corresponding box element, and not for example edit buttons of any nested boxes.

Note that this Javascript code is rendered as a Jinja template and placed directly in the html page on the browser. Hence, component attributes are available in 
the Jinja variable "compo", e.g. {{ compo.cid }} 

The code that is executed once a click is detected, creates an EPFL event for our component with the name "edit_note" and calls sends the event to the server.
Since EPFL event handling methods have to preceded by "handle\_" in the server code, our existing "handle_edit_note" method is called and the "Edit note" form is 
filled with the values of the selected note. Voilà!

This completes our tutorial. In this part of the tutorial, you have learned to design complex nested components, to adapt themed templates,
and to extend the Javascript part of a component to detect Browser events and send EPFL to the server. 