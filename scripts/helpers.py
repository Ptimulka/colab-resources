import os
import tensorflow as tf
from termcolor import colored
from IPython.display import Image
from ipywidgets import interact, interact_manual


def choose_style_from_existing(dirpath, style_info):
    @interact
    def show_images(file=os.listdir(dirpath)):
        url = dirpath + file
        style_info.name = file
        display(Image(url, width=500))


def set_device(device_info):
    if tf.test.is_gpu_available():
        device_info.device = '/gpu:0'
        print(colored("GPU will be used.", 'green'))
    elif 'COLAB_TPU_ADDR' in os.environ:
        device_info.device = "tpu"
        print(colored("TPU will be used.", 'green'))
    else:
        print(colored("Neither GPU nor TPU is available! Choose one of them from Runtime -> Change runtime type, and run all cells again.", 'red'))
