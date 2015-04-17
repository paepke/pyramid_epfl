from solute.epfl.components import Button

class Download(Button):
    """
    This component provides basic download button functionality.

    To use a download button, a event handling method for handling the button clicks has to be provided:

    .. code:: python

        download = Download(name="Do something", event_name="submit")

        def handle_submit(self):
            file = [data, filename]
            self.return_ajax_response(file)
            # get the data that should be downloaded and return them using ajax

    """

    asset_spec = "solute.epfl.components:download/static"

    js_parts = ["download/download.js"]
    js_name = ["download.js",
               "FileSaver.min.js"]
