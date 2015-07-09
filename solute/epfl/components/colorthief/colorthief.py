# * encoding: utf-8

from solute.epfl.components.form.form import FormInputBase
from urllib2 import urlopen
import io
import random

try:
    from PIL import Image
    import numpy
    dependency_error = False
except ImportError:
    dependency_error = True


# Source: http://blog.zeevgilovitz.com/detecting-dominant-colours-in-python/
#################################################
class Cluster(object):
    def __init__(self):
        self.pixels = []
        self.centroid = None

    def addPoint(self, pixel):
        self.pixels.append(pixel)

    def setNewCentroid(self):

        R = [colour[0] for colour in self.pixels]
        G = [colour[1] for colour in self.pixels]
        B = [colour[2] for colour in self.pixels]
        try:
            R = sum(R) / len(R)
        except ZeroDivisionError:
            R = 0
        try:
            G = sum(G) / len(G)
        except ZeroDivisionError:
            G = 0
        try:
            B = sum(B) / len(B)
        except ZeroDivisionError:
            B = 0

        self.centroid = (R, G, B)
        self.pixels = []

        return self.centroid

# Source: http://blog.zeevgilovitz.com/detecting-dominant-colours-in-python/
#################################################
class Kmeans(object):
    def __init__(self, k=3, max_iterations=5, min_distance=5.0, size=200):
        self.k = k
        self.max_iterations = max_iterations
        self.min_distance = min_distance
        self.size = (size, size)

    def run(self, image):
        self.image = image
        self.image.thumbnail(self.size)
        self.pixels = numpy.array(image.getdata(), dtype=numpy.uint8)

        self.clusters = [None for i in range(self.k)]
        self.oldClusters = None

        randomPixels = random.sample(self.pixels, self.k)

        for idx in range(self.k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = randomPixels[idx]

        iterations = 0

        while self.shouldExit(iterations) is False:

            self.oldClusters = [cluster.centroid for cluster in self.clusters]

            for pixel in self.pixels:
                self.assignClusters(pixel)

            for cluster in self.clusters:
                cluster.setNewCentroid()

            iterations += 1

        return [cluster.centroid for cluster in self.clusters]

    def assignClusters(self, pixel):
        shortest = float('Inf')
        for cluster in self.clusters:
            distance = self.calcDistance(cluster.centroid, pixel)
            if distance < shortest:
                shortest = distance
                nearest = cluster

        nearest.addPoint(pixel)

    def calcDistance(self, a, b):
        result = numpy.sqrt(sum((a - b) ** 2))
        return result

    def shouldExit(self, iterations):
        if self.oldClusters is None:
            return False

        for idx in range(self.k):
            dist = self.calcDistance(
                numpy.array(self.clusters[idx].centroid),
                numpy.array(self.oldClusters[idx])
            )
            if dist < self.min_distance:
                return True

        if iterations <= self.max_iterations:
            return False

        return True


def get_dominant_colors_from_url(url, color_count=8):
    """Fetch the image from the url and extract the dominant colors

    :param url: image url
    :param color_count: count of dominant colors
    """
    path = io.BytesIO(urlopen(url).read())
    im_ex = Image.open(path)
    kk = Kmeans(k=color_count)
    return kk.run(im_ex)


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"
    js_parts = []
    compo_state = FormInputBase.compo_state + ["image_src", "dominat_colors_count"]

    height = None  #: Compo height in px if none nothing is set

    width = None  #: Compo width in px if none nothing is set

    image_src = None  #: image src if set the drop zone is hidden

    color_count = 7  #: Count of colors which got extracted from the image

    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'color_count']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click', 'handle_drop']

    def __init__(self, page, cid, height=None, width=None, image_src=None, color_count=None, **extra_params):
        """ColorThief Compo: A Drop Area where images can be dropped and their colors get extracted

        :param height: Compo height in px if none nothing is set
        :param width: Compo width in px if none nothing is set
        :param image_src: image src if set the drop zone is hidden
        :param color_count: Count of colors which got extracted from the image
        :return:
        """
        if dependency_error:
            raise ImportError("ColorThief Component has pillow and numpy as dependency")
        super(ColorThief, self).__init__(page=page, cid=cid, height=height, width=width, image_src=image_src,
                                         color_count=color_count, **extra_params)

    def handle_change(self, value, image_src=None):
        if image_src is not None:
            dominant_colors = set(get_dominant_colors_from_url(image_src, color_count=self.color_count))
            self.value = [{"rgb": "#%x%x%x" % (val[0], val[1], val[2]), "selected": False} for val in dominant_colors]
        else:
            self.value = None
        self.image_src = image_src
        self.redraw()

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')

    def handle_click_color(self, color):
        for val in self.value:
            if val["rgb"] == color:
                val["selected"] = not val["selected"]
                break

        self.redraw()
