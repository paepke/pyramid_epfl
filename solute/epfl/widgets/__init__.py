from autocomplete.autocomplete import AutocompleteWidget
from suggest.suggest import SuggestWidget
from accordion.accordion import AccordionWidget
from datepicker.datepicker import DatepickerWidget
from datetimepicker.datetimepicker import DatetimepickerWidget
from slider.slider import SliderWidget
from spinner.spinner import Spinner, SpinnerWidget
from image_selector.image_selector import ImageSelectorWidget
from ckeditor.ckeditor import CKEditorWidget
from basic.basic import ButtonWidget
from sort.sort import SortWidget
from upload.upload import UploadWidget
from download.download import DownloadWidget
from progress.progress import ProgressWidget
from toggle.toggle import ToggleWidget



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
    DatetimepickerWidget.add_pyramid_routes(config)
    SpinnerWidget.add_pyramid_routes(config)
    DownloadWidget.add_pyramid_routes(config)
    ProgressWidget.add_pyramid_routes(config)
    ToggleWidget.add_pyramid_routes(config)
