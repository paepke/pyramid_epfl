from autocomplete.autocomplete import AutocompleteWidget
from suggest.suggest import SuggestWidget
from accordion.accordion import AccordionWidget
from datepicker.datepicker import DatepickerWidget
from slider.slider import SliderWidget
from image_selector.image_selector import ImageSelectorWidget
from ckeditor.ckeditor import CKEditorWidget
from basic.basic import ButtonWidget
from sort.sort import SortWidget
from upload.upload import UploadWidget




def add_routes(config):
    AutocompleteWidget.add_pyramid_routes(config)
    SuggestWidget.add_pyramid_routes(config)
    AccordionWidget.add_pyramid_routes(config)
    DatepickerWidget.add_pyramid_routes(config)
    SliderWidget.add_pyramid_routes(config)
    ImageSelectorWidget.add_pyramid_routes(config)
    CKEditorWidget.add_pyramid_routes(config)
    ButtonWidget.add_pyramid_routes(config)
    SortWidget.add_pyramid_routes(config)
    UploadWidget.add_pyramid_routes(config)
