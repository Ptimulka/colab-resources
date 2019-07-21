import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10,10)
mpl.rcParams['axes.grid'] = False

import numpy as np
from PIL import Image
import time
import functools
import uuid
import os
import math
import sys
import IPython
import warnings
warnings.filterwarnings("error")
from termcolor import colored
from urllib.parse import urlparse

import ipywidgets as widgets

import tensorflow as tf
import tensorflow.contrib.eager as tfe

from tensorflow.python.keras.preprocessing import image as kp_image
from tensorflow.python.keras import models
from tensorflow.python.keras import losses
from tensorflow.python.keras import layers
from tensorflow.python.keras import backend as K

tf.enable_eager_execution()


class ImageInfo(object):
    def __init__(self, path=None):
        self.gdrivepath = None
        self.scale = None


image_info = ImageInfo()
style_info = ImageInfo()
