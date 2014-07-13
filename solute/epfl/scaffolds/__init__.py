
from pyramid.scaffolds import PyramidTemplate

class EPFLStarterTemplate(PyramidTemplate):
    _template_dir = 'epfl_starter_scaffold'
    summary = 'EPFL barebone application'

class EPFLDemoTemplate(PyramidTemplate):
    _template_dir = 'epfl_demo_scaffold'
    summary = 'EPFL demo application'

class EPFLNotesTemplate(PyramidTemplate):
    _template_dir = 'epfl_notes_scaffold'
    summary = 'EPFL notes application'

