# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl

from solute.epfl.components import Box
from solute.epfl.components import cfForm
from solute.epfl.components import cfNumber
from solute.epfl.components import cfText
from solute.epfl.components import cfTextarea
from solute.epfl.components import cfButton
from solute.epfl.components import NavLayout

from solute.epfl.components import LinkListLayout

from solute.epfl.core.epflassets import ModelBase
from solute.epfl.core.epflcomponentbase import ComponentBase

from .first_step import FirstStepRoot


class MyFirstForm(cfForm):
    node_list = [cfNumber(label='Parent',
                          name='parent'),
                 cfText(label='Title',
                        name='title'),
                 cfTextarea(label='Text',
                            name='text'),
                 cfButton(value='Submit',
                          event_name='submit'),
                 cfButton(value='Cancel',
                          event_name='cancel')]

    compo_state = cfForm.compo_state[:]
    compo_state.append('id')
    id = None

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


class NoteBox(Box):
    is_removable = True
    data_interface = {'id': None,
                      'text': None,
                      'children': None,
                      'title': '{title} - ({id})'}

    theme_path = Box.theme_path[:]
    theme_path.append('<epfl_pyramid_barebone:templates/theme/note')

    js_parts = Box.js_parts[:]
    js_parts.append('epfl_pyramid_barebone:templates/theme/note/note.js')


    def __init__(self, *args, **kwargs):
        super(NoteBox, self).__init__(*args, **kwargs)
        self.get_data = 'note_children'
        self.default_child_cls = NoteBox

    def handle_edit_note(self):
        self.page.my_first_form.load_note(self.id)

    def handle_removed(self):
        super(NoteBox, self).handle_removed()
        self.page.model.remove_note(self.id)


class MyModel(ModelBase):
    data_store = {'_id_counter': 1,
                  '_id_lookup': {}}

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        note.setdefault('children', [])

        self.data_store['_id_lookup'][note['id']] = note

        if note['parent'] != 0:
            self.get_note(note['parent']).setdefault('children', []).append(note['id'])
        else:
            self.data_store.setdefault('notes', []).append(note)

    def remove_note(self, note_id):
        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]
        parent = self.data_store['_id_lookup'].pop(note_id)['parent']
        self.get_note(parent)['children'].remove(note_id)

    def get_note(self, note_id):
        return self.data_store['_id_lookup'][note_id]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        notes = self.data_store.get('notes', [])
        return notes

    def load_note_children(self, calling_component, *args, **kwargs):
        return [self.get_note(child_id) for child_id in self.get_note(calling_component.id)['children']]


class SecondStepRoot(FirstStepRoot):
    def init_struct(self):
        self.node_list.extend([Box(title='My first box',
                                   node_list=[MyFirstForm(cid='my_first_form')]),
                               LinkListLayout(get_data='notes',
                                              show_pagination=False,
                                              show_search=False,
                                              node_list=[ComponentBase(url='/',
                                                                       text='Home'),
                                                         ComponentBase(url='/second',
                                                                       text='Second',
                                                                       static_align='bottom')],
                                              data_interface={'id': None,
                                                              'url': 'note?id={id}',
                                                              'text': 'title'},
                                              slot='west'),
                               Box(title='My notes',
                                   default_child_cls=NoteBox,
                                   data_interface=NoteBox.data_interface,
                                   get_data='notes')])


@view_config(route_name='SecondStep')
class SecondStepPage(epfl.Page):
    root_node = SecondStepRoot()
    model = MyModel