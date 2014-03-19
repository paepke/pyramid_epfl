from autocomplete.autocomplete import AutoComplete, AutocompleteWidget
from datepicker.datepicker import DatepickerWidget
from slider.slider import SliderWidget
from image_selector.image_selector import ImageSelectorWidget
from ckeditor.ckeditor import CKEditorWidget
from basic.basic import ButtonWidget
from sort.sort import Sort, SortWidget
from basic.basic import Button, Entry, TextArea, Select




def add_static_routes(config):
    for path in ["autocomplete",
                 "datepicker",
                 "slider",
                 "image_selector",
                 "ckeditor",
                 "basic",
                 "sort"]:
        config.add_static_view(name = "epfl/widgets/" + path, path = "solute.epfl.widgets:" + path + "/static")

