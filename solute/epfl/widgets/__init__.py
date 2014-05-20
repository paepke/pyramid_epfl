from autocomplete.autocomplete import AutoComplete, AutocompleteWidget
from suggest.suggest import Suggest, SuggestWidget
from accordion.accordion import Accordion, AccordionWidget
from datepicker.datepicker import DatepickerWidget
from timepicker.timepicker import Timepicker, TimepickerWidget
from slider.slider import SliderWidget
from image_selector.image_selector import ImageSelectorWidget
from ckeditor.ckeditor import CKEditorWidget
from basic.basic import ButtonWidget
from sort.sort import Sort, SortWidget
from basic.basic import Button, Entry, TextArea, Select, RadioButton, ButtonSet, Checkbox




def add_static_routes(config):
    for path in ["autocomplete",
                 "suggest",
                 "datepicker",
                 "timepicker",
                 "slider",
                 "image_selector",
                 "ckeditor",
                 "basic",
                 "sort",
                 "accordion"]:
        config.add_static_view(name = "epfl/widgets/" + path, path = "solute.epfl.widgets:" + path + "/static")

