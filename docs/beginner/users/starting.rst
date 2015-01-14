.. code-block:: bash

    pcreate -s pyramid_epfl_starter demo_app
    cd demo_app/
    python setup.py develop
    pserve development.ini --reload


.. code-block:: python

    node_list = [Box(title='My first box')]

tid löschen

.. code-block:: python

    constrained = True


.. code-block:: python

    node_list = [Box(title='My first box',
                     node_list=[cfForm(cid='my_first_form')])]


.. code-block:: python

    from solute.epfl.components import cfText
    from solute.epfl.components import cfTextarea
    from solute.epfl.components import cfButton


.. code-block:: python

    node_list = [Box(title='My first box',
                     node_list=[cfForm(cid='my_first_form',
                                       node_list=[cfText(label='Title',
                                                         name='title',
                                                         default='Insert a title here!'),
                                                  cfTextarea(label='Text',
                                                             name='text'),
                                                  cfButton(value='Submit',
                                                           event_name='submit')])])]

.. code-block:: python

    class MyFirstForm(cfForm):
        cid = 'my_first_form',
        node_list = [cfText(label='Title',
                            name='title',
                            default='Insert a title here!'),
                     cfTextarea(label='Text',
                                name='text'),
                     cfButton(value='Submit',
                              event_name='submit')]

.. code-block:: python
    node_list = [Box(title='My first box',
                     node_list=[MyFirstForm()])]

.. code-block:: python

    def handle_submit(self):
        if not self.validate():
            self.page.show_fading_message('An error occurred in validating the form!', 'error')
            return
        print self.get_values()

.. code-block:: python

    class MyModel(ModelBase):
        pass

    @view_config(route_name='home')
    class HomePage(epfl.Page):
        root_node = HomeRoot()
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
