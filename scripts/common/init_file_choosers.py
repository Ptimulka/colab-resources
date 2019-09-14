import os
import math
import uuid
import IPython
from PIL import Image
import ipywidgets as widgets
from termcolor import colored
from urllib.parse import urlparse

# TODO move somewhere and update code

def upload_file(image_info):
    from google.colab import files
    uploaded = files.upload()

    if (len(uploaded.keys()) != 0):
        filename = next(iter(uploaded.keys()))
        newfilename = str(uuid.uuid4()) + filename

        !mv "$filename" "$newfilename"
        !mv "$newfilename" "$input_gdrive_path"

        image_info.gdrivepath = input_gdrive_path + "/" + newfilename


class ImageSizeChooser(object):

    def load_img_size(self, path_to_img, scale):
        img = Image.open(path_to_img)
        img = img.resize((round(img.size[0] * scale), round(img.size[1] * scale)), Image.ANTIALIAS)
        return img.size

    def init_recommended(self):
        try:
            width, height = self.load_img_size(image_info.gdrivepath, 1)
            with self.out:
                self.original_info = "Original image size is: " + str(width) + "x" + str(height)
                longer = max(width, height)
                recommended_longer = 512
                if (longer > recommended_longer):
                    self.recommended_scale = round(100 * float(recommended_longer) / longer)
                    self.recommended_info = colored(
                        "We recommend to change image size to " + str(self.recommended_scale) + "%", 'green')
                else:
                    self.recommended_scale = 100
        except:
            print(colored("Error occured, probably the image is not selected.", 'red'))

    def __init__(self, image_info):
        self.out = widgets.Output()
        self.image_info = image_info
        IPython.display.display(self.out)
        self.init_recommended()

    def widget(self):

        def on_click_custom_scale(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                try:
                    print(self.original_info)
                    if (self.recommended_info is not None):
                        print(self.recommended_info)
                    print(colored("Scale set to " + str(self.scale_slider.value) + "%", 'green'))
                    width, height = self.load_img_size(image_info.gdrivepath, float(self.scale_slider.value) / 100)
                    print("Image size: " + str(width) + "x" + str(height))
                    IPython.display.display(IPython.display.Image(image_info.gdrivepath, width=width))
                    self.image_info.scale = self.scale_slider.value
                except:
                    print(colored("Error occured, probably the image is not selected.", 'red'))

        self.scale_slider = widgets.IntSlider(
            value=self.recommended_scale,
            min=5,
            max=100,
            step=1,
            description='Scale:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )

        box = widgets.VBox()
        self.button = widgets.Button(description="Apply scale")
        self.button.on_click(on_click_custom_scale)
        box.children = [self.scale_slider, self.button]
        on_click_custom_scale(self.button)
        return box