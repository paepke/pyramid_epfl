# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl

from solute.epfl.components import Box
from solute.epfl.components import cfForm
from solute.epfl.components import cfText
from solute.epfl.components import cfTextarea
from solute.epfl.components import cfButton
from solute.epfl.components import NavLayout

from solute.epfl.components import LinkListLayout

from solute.epfl.core.epflassets import ModelBase
from solute.epfl.core.epflcomponentbase import ComponentBase


class NoteForm(cfForm):
    node_list = [cfText(label='Title',
                        name='title',
                        default='Insert a title here!'),
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
        note_value = {'title': values['title'],
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
        self.redraw()

    def load_note(self, note_id):
        note = self.page.model.get_note(note_id)
        self.id = note['id']
        self.set_value('title', note['title'])
        self.set_value('text', note['text'])
        self.redraw()


class NoteBox(Box):
    data_interface = {'id': None,
                      'text': None,
                      'title': None}
    is_removable = True

    def init_struct(self):
        self.node_list.append(ComponentBase(template_name='epfl_pyramid_barebone:templates/note.html'))
        self.node_list.append(cfButton(value='Edit this note',
                                       event_name='edit_note'))

    def handle_edit_note(self):
        self.page.note_form.load_note(self.id)

    def handle_removed(self):
        super(NoteBox, self).handle_removed()
        self.page.model.remove_note(self.id)


class NoteModel(ModelBase):
    data_store = {'_id_counter': 1}

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        self.data_store.setdefault('notes', []).append(note)

    def remove_note(self, note_id):
        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]

    def get_note(self, note_id):
        return [note for note in self.data_store['notes'] if note['id'] == note_id][0]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        return self.data_store.get('notes', [])


class FirstStepRoot(epfl.components.CardinalLayout):
    constrained = True

    node_list = [NavLayout(slot='north',
                           links=[('Second Step', '/second')],
                           title='Demo Notes App')]

    def init_struct(self):
        self.node_list.extend([Box(title='Edit note',
                                   node_list=[NoteForm(cid='note_form')]),
                               Box(title='My notes',
                                   default_child_cls=NoteBox,
                                   data_interface={'id': None,
                                                   'text': None,
                                                   'title': None},
                                   get_data='notes'),
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
                                              slot='west')])


@view_config(route_name='FirstStep')
class FirstStepPage(epfl.Page):
    root_node = FirstStepRoot()
    model = NoteModel
