# coding: utf-8
from solute.epfl.core import epflcomponentbase

class Progress(epflcomponentbase.ComponentBase):

    """
    This component display a progress bar.

    Use it code like this:

    .. code:: python

        progress = Progress(min=0, max=100, value=70)

   """

    template_name = "progress/progress.html"

    compo_state = ["value", "min", "max", "color"]


    value = 0  #: The value of the progress bar
    min = 0  #: The min value of the progress bar
    max = 100  #: The max value of the progress bar
    color = "default"  #: color of the progress bar (can be "default", "info", "warning", "danger", "success"
    hide_value_label = False  #: Set to True if value label should not be printed

    def __init__(self, page, cid, value=None, min=False, max=None, color=None, hide_value_label=False, **extra_params):
        """A component that display a progress bar.

        :param value: The value of the progress bar
        :param min: The min value of the progress bar
        :param max: The max value of the progress bar
        :param color: The color of the progress bar
        :param hide_value_label: Set to True if value label should not be printed
        """
        super(Progress, self).__init__()


class StackedProgress(epflcomponentbase.ComponentBase):

    """
    This component display a stacked progress bar. Each progress bar has to be defined as a tuple (width, color), where
    width is a percentage width (full width is 100%)
    and color is a bootstrap progress bar class (e.g. "progress-bar-success", "progress-bar-warning progress-bar-striped"

    Use it code like this:

    .. code:: python

        progress = StackedProgress(value=[(20, "progress-bar-success"), (30, "progress-bar-warning progress-bar-striped")])

   """

    template_name = "progress/stacked_progress.html"

    compo_state = ["value"]


    value = []  #: A list if tuples defining the stacked progress bars

    def __init__(self, page, cid, value=None, **extra_params):
        """A component that display a stacked progress bar.

        :param value: The value of the progress bar
        """
        super(StackedProgress, self).__init__(page, cid,
                                              value=value,
                                              **extra_params)
